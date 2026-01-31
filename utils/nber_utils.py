# -*- coding: utf-8 -*-
"""
nber_utils.py — NBER Business Cycle Dating Committee (BCDC) recession dates loader

사용 예 (Colab):
----------------
import sys
sys.path.append("/content/drive/MyDrive/Colab Notebooks/book_FinancialEconomics/utils")

import nber_utils as nu
nu.bind_env(globals())

url = "https://www.nber.org/sites/default/files/2023-03/BCDC_spreadsheet_for_website.xlsx"
NBERm, NBERq = nu.load_and_process_nber_data(url)
print(NBERm.tail(8))
"""

import re
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 내부 파싱 함수
# -----------------------------
MONTH_NAME_RE = re.compile(r'^([A-Za-z]+)')
YEAR_RE       = re.compile(r'(\d{4})')
QSTR_RE       = re.compile(r'\((\d{4}Q[1-4])\)')

def _parse_cell(s):
    """
    Parse one cell like 'November (1948Q4)' or 'February 2020'.
    Returns dict with: month_num, year, qstr (may be None)
    """
    out = dict(month_num=None, year=None, qstr=None)
    if not isinstance(s, str):
        return out
    s = s.strip()
    m = MONTH_NAME_RE.search(s)
    if m:
        mon = m.group(1)
        try:
            out["month_num"] = pd.to_datetime(mon, format="%B").month
        except Exception:
            try:
                out["month_num"] = pd.to_datetime(mon, format="%b").month
            except Exception:
                out["month_num"] = None
    y = YEAR_RE.search(s)
    if y:
        out["year"] = int(y.group(1))
    q = QSTR_RE.search(s)
    if q:
        out["qstr"] = q.group(1)  # 'YYYYQx'
    return out


# -----------------------------
# NBER 경기침체 데이터 로더
# -----------------------------
def load_and_process_nber_data(url):
    """
    Load NBER recession peaks & troughs from the spreadsheet.
    Accepts rows like 'Month (YYYYQx)' or 'Month YYYY'.
    Returns:
      - NBERm: monthly DataFrame with columns ['peak', 'trough']
      - NBERq: quarterly DataFrame with columns ['peak', 'trough']
    """
    raw = pd.read_excel(url, sheet_name=0, header=None)

    # 후보 블록 탐색: 인접한 두 컬럼이 모두 "월 + 연도/분기" 형태인 행만 모음
    candidates = []
    for c in range(raw.shape[1]-1):
        A = raw[c].astype(str).str.strip()
        B = raw[c+1].astype(str).str.strip()

        def looks_like_token(s):
            return s.str.match(r'^[A-Za-z]+', na=False) & s.str.contains(r'\d{4}', na=False)

        mask = looks_like_token(A) & looks_like_token(B)
        rows = raw.loc[mask, [c, c+1]].copy()
        if not rows.empty:
            rows.columns = ['peak_raw', 'trough_raw']
            candidates.append(rows)

    if not candidates:
        # 관대한 백업 범위 (최근 연도 포함 가능)
        block = raw.iloc[4:400, 2:4].copy()
        block.columns = ['peak_raw', 'trough_raw']
    else:
        block = pd.concat(candidates, axis=0).drop_duplicates().reset_index(drop=True)

    # 파싱
    parsed_peak   = block['peak_raw'].apply(_parse_cell).apply(pd.Series)
    parsed_trough = block['trough_raw'].apply(_parse_cell).apply(pd.Series)
    parsed_peak.columns   = [f'peak_{c}' for c in parsed_peak.columns]
    parsed_trough.columns = [f'trough_{c}' for c in parsed_trough.columns]
    df = pd.concat([parsed_peak, parsed_trough], axis=1)

    # --- 월별 ---
    NBERm = pd.DataFrame(index=df.index, columns=['peak','trough'], dtype='datetime64[ns]')
    pmask = df['peak_month_num'].notna() & df['peak_year'].notna()
    tmask = df['trough_month_num'].notna() & df['trough_year'].notna()

    if pmask.any():
        NBERm.loc[pmask, 'peak'] = pd.to_datetime(
            {'year': df.loc[pmask, 'peak_year'].astype(int),
             'month': df.loc[pmask, 'peak_month_num'].astype(int),
             'day': 1}
        )
    if tmask.any():
        NBERm.loc[tmask, 'trough'] = pd.to_datetime(
            {'year': df.loc[tmask, 'trough_year'].astype(int),
             'month': df.loc[tmask, 'trough_month_num'].astype(int),
             'day': 1}
        )
    NBERm = NBERm.dropna().reset_index(drop=True)

    # --- 분기별 ---
    def to_quarter_start(y, m):
        q = ((m-1)//3) + 1
        return pd.Period(f"{int(y)}Q{int(q)}", freq='Q-DEC').to_timestamp(how='start')

    NBERq = pd.DataFrame(columns=['peak','trough'])

    # peak
    peak_q = pd.Series(pd.NaT, index=df.index, dtype='datetime64[ns]')
    mask_qp = df['peak_qstr'].notna()
    if mask_qp.any():
        pi = pd.PeriodIndex(df.loc[mask_qp, 'peak_qstr'], freq='Q-DEC')
        peak_q.loc[mask_qp] = pi.to_timestamp(how='start')
    mask_infer_p = (~mask_qp) & df['peak_year'].notna() & df['peak_month_num'].notna()
    if mask_infer_p.any():
        peak_q.loc[mask_infer_p] = [
            to_quarter_start(y, m) for y, m in
            zip(df.loc[mask_infer_p, 'peak_year'], df.loc[mask_infer_p, 'peak_month_num'])
        ]

    # trough
    trough_q = pd.Series(pd.NaT, index=df.index, dtype='datetime64[ns]')
    mask_qt = df['trough_qstr'].notna()
    if mask_qt.any():
        pi = pd.PeriodIndex(df.loc[mask_qt, 'trough_qstr'], freq='Q-DEC')
        trough_q.loc[mask_qt] = pi.to_timestamp(how='start')
    mask_infer_t = (~mask_qt) & df['trough_year'].notna() & df['trough_month_num'].notna()
    if mask_infer_t.any():
        trough_q.loc[mask_infer_t] = [
            to_quarter_start(y, m) for y, m in
            zip(df.loc[mask_infer_t, 'trough_year'], df.loc[mask_infer_t, 'trough_month_num'])
        ]

    NBERq['peak'] = peak_q
    NBERq['trough'] = trough_q
    NBERq = NBERq.dropna().reset_index(drop=True)

    print("✅ NBER recession data loaded successfully.")
    print(f"📅 Number of cycles detected: {len(NBERm)}")
    return NBERm, NBERq


# -----------------------------
# Recession shading function
# -----------------------------
def plot_nber_recession(
    ax,
    nber_df,
    color='gray',
    alpha=0.3,
    label='_nolegend_',
    clip_to_xlim=True,
    keep_xlim=True
):
    """
    Highlight NBER recession periods on a Matplotlib Axes.

    왜 이런 옵션이 필요한가?
    - nber_df에는 1850년대 등 매우 과거 구간이 포함될 수 있습니다.
      이때 ax.axvspan()을 그대로 그리면 Matplotlib autoscale 때문에 x축이 과거로 확장될 수 있습니다.
    - clip_to_xlim=True: 현재 화면(xlim)과 겹치는 recession만 그려서 축 확장을 방지합니다.
    - keep_xlim=True: 그리기 전 xlim을 저장했다가 끝나고 복구합니다.

    주의(빈 축에 shading만 그리는 경우):
    - ax에 아직 데이터가 하나도 없으면 기본 xlim이 (0, 1) 같은 숫자 범위라서,
      clip_to_xlim/keep_xlim 로직이 shading을 "전부 스킵"시키거나 결과가 안 보일 수 있습니다.
      이 경우에는 자동으로 (i) clip_to_xlim=False, keep_xlim=False로 전환하고
      (ii) NBER 데이터의 전체 범위를 xlim으로 설정합니다.
    """
    if nber_df is None or len(nber_df) == 0:
        return

    # NBER 전체 범위
    nber_start = pd.to_datetime(nber_df["peak"].min())
    nber_end = pd.to_datetime(nber_df["trough"].max())

    # ✅ 빈 축(데이터 없음)이라면: recession shading만 보여주는 예시를 위해 자동 처리
    if not ax.has_data():
        clip_to_xlim = False
        keep_xlim = False
        ax.set_xlim(nber_start, nber_end)

        # 예시 코드에서 legend를 쓰는 경우가 많으니,
        # 사용자가 label을 따로 안 줬고(_nolegend_) 축이 비어있으면 기본 라벨을 부여
        if label == "_nolegend_":
            label = "NBER recession"

    # 현재 xlim 저장 (Matplotlib 내부 단위 float일 수도 있으므로 그대로 저장)
    xlim0 = ax.get_xlim()

    # clipping을 위해 현재 xlim을 datetime으로 변환 (가능할 때만)
    xmin_dt = xmax_dt = None
    if clip_to_xlim:
        try:
            import matplotlib.dates as mdates
            xmin_num, xmax_num = ax.get_xlim()
            xmin_dt = pd.Timestamp(mdates.num2date(xmin_num).replace(tzinfo=None))
            xmax_dt = pd.Timestamp(mdates.num2date(xmax_num).replace(tzinfo=None))
        except Exception:
            clip_to_xlim = False

    first = True
    for _, row in nber_df.iterrows():
        peak = row.get("peak", pd.NaT)
        trough = row.get("trough", pd.NaT)
        if pd.isna(peak) or pd.isna(trough):
            continue

        peak = pd.Timestamp(peak)
        trough = pd.Timestamp(trough)

        if clip_to_xlim and (xmin_dt is not None) and (xmax_dt is not None):
            # 화면 범위와 겹치지 않으면 skip
            if trough < xmin_dt or peak > xmax_dt:
                continue
            # 겹치면 화면 범위로 클립
            peak_draw = max(peak, xmin_dt)
            trough_draw = min(trough, xmax_dt)
        else:
            peak_draw, trough_draw = peak, trough

        ax.axvspan(
            peak_draw,
            trough_draw,
            color=color,
            alpha=alpha,
            label=(label if first else None)
        )
        first = False

    # xlim 복구(축 확장 방지)
    if keep_xlim:
        ax.set_xlim(xlim0)

    # print("✅ NBER recession shading applied.")

# -----------------------------
# Colab-safe 주입 유틸 (선택)
# -----------------------------
def export_env():
    """노트북 전역(globals)에 주입할 객체 묶음을 dict로 반환."""
    return dict(
        load_and_process_nber_data=load_and_process_nber_data,
        plot_nber_recession=plot_nber_recession,
        pd=pd, plt=plt
    )

def bind_env(ns):
    """원하는 네임스페이스(보통 globals())에 nber 관련 함수/객체를 주입."""
    ns.update(export_env())


# -----------------------------
# 로드 완료 메시지
# -----------------------------
print("✅ nber_utils ready (functions: load_and_process_nber_data, plot_nber_recession)")
