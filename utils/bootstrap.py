# -*- coding: utf-8 -*-
"""
bootstrap.py — 모든 장 노트북이 공통으로 부르는 '환경 초기화' 진입점.

이 파일 하나가 지금까지 각 노트북 첫 3개 셀에 복사돼 있던 준비 코드
(경로 감지 · 패키지 설치 · preamble_core 세팅 · koreanize · ECOS 키 · NBER 로딩)를
모두 담당합니다. 개선 사항을 여기서 한 번만 고치면 전 장에 반영됩니다.

노트북 첫 셀(모든 장 동일):
--------------------------------
import os, sys

# 리포 루트 자동 감지: (1) 이미 clone됨 → (2) Google Drive(저자) → (3) 자동 clone → (4) 로컬
if os.path.isdir("/content") and not os.path.exists("/content/resources"):
    try:
        from google.colab import drive
        drive.mount("/content/drive")
    except Exception:
        pass

_DRIVE = "/content/drive/MyDrive/Colab Notebooks/book_FinancialEconomics"
if os.path.exists("/content/resources"):
    ROOT = "/content/resources"          # 독자: git clone 방식(README 방법 A)
elif os.path.isdir(_DRIVE):
    ROOT = _DRIVE                        # 저자: Google Drive 방식
elif os.path.isdir("/content"):
    os.system("git clone -q https://github.com/FinancialEconomicsPython/resources.git /content/resources")
    ROOT = "/content/resources"          # 독자: 자동 clone
else:
    ROOT = os.getcwd()                   # 로컬 실행

sys.path.insert(0, os.path.join(ROOT, "utils"))
from bootstrap import init
env = init(globals(), root=ROOT, ecos_key="YOUR_ECOS_API_KEY_HERE")
--------------------------------

init()이 반환하는 env(SimpleNamespace)에는 ROOT/UTILS/FIGS/DATA/ecos_key와,
load_nber=True면 NBERm/NBERq가 담깁니다. 동시에 노트북 전역(globals)에는
np/pd/plt/save_fig/plot_dual_axis/NBER 함수·데이터가 주입됩니다(기존 동작 유지).
"""

import os
import sys
import subprocess
import importlib
from types import SimpleNamespace

# NBER 침체구간 스프레드시트(연도 경로가 바뀌면 여기만 수정, 실패 시 data/ 사본으로 폴백)
NBER_URL = "https://www.nber.org/sites/default/files/2023-03/BCDC_spreadsheet_for_website.xlsx"
NBER_LOCAL = "data/BCDC_spreadsheet_for_website.xlsx"  # ROOT 기준 상대경로(있으면 폴백)


# -----------------------------
# 내부 헬퍼
# -----------------------------
def _in_colab():
    return "google.colab" in sys.modules or os.path.isdir("/content")


def _pip_install_if_missing(module_name, pip_name=None):
    """모듈이 import 안 되면 조용히 pip 설치. (매 실행 !pip 반복 방지)"""
    try:
        importlib.import_module(module_name)
        return False
    except Exception:
        pip_name = pip_name or module_name
        print(f"📦 installing {pip_name} ...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", pip_name],
            check=False,
        )
        return True


def _resolve_ecos_key(ecos_key):
    """
    ECOS 키 결정 우선순위:
      1) Colab Secrets(🔑)에 저장된 'ECOS_API_KEY'  ← 노트북에 평문 저장 안 함(권장)
      2) 인자로 넘어온 ecos_key (플레이스홀더가 아니면)
    유효한 키가 없으면 None을 반환(호출부에서 필요 시 안내).
    """
    PLACEHOLDER = "YOUR_ECOS_API_KEY_HERE"

    # 1) Colab Secrets 우선
    try:
        from google.colab import userdata
        secret = userdata.get("ECOS_API_KEY")
        if secret:
            return secret
    except Exception:
        pass

    # 2) 인자
    if ecos_key and PLACEHOLDER not in ecos_key:
        return ecos_key

    return None


# -----------------------------
# 메인 진입점
# -----------------------------
def init(
    namespace=None,
    root=None,
    ecos_key=None,
    require_ecos=False,
    load_nber=True,
    seaborn=True,
    screen_dpi=100,
    save_dpi=600,
):
    """
    노트북 환경을 한 번에 초기화한다.

    Parameters
    ----------
    namespace : dict
        노트북의 globals(). np/pd/plt/save_fig/plot_dual_axis 등을 여기에 주입한다.
    root : str
        리포 루트(첫 셀에서 감지해 넘김). None이면 자동 감지.
    ecos_key : str
        한국은행 ECOS API 키(플레이스홀더면 무시). Colab Secrets가 우선.
    require_ecos : bool
        True면 유효한 ECOS 키가 없을 때 실행을 멈춘다(ECOS가 꼭 필요한 장).
        False(기본)면 경고만 하고 계속한다 → ECOS를 안 쓰는 장이 첫 셀에서
        멈추던 기존 버그를 방지.
    load_nber : bool
        NBER 침체구간 데이터를 불러와 env/namespace에 NBERm/NBERq로 넣을지.
    seaborn : bool
        seaborn 스타일 사용 여부.

    Returns
    -------
    env : SimpleNamespace
        ROOT/UTILS/FIGS/DATA/ecos_key (+ load_nber면 NBERm/NBERq).
    """
    # --- 1) 경로 확정 ---
    if root is None:
        root = os.getcwd()
    UTILS = os.path.join(root, "utils")
    FIGS = os.path.join(root, "figures")
    DATA = os.path.join(root, "data")
    if UTILS not in sys.path:
        sys.path.insert(0, UTILS)

    # --- 2) 패키지 설치(없을 때만) ---
    _pip_install_if_missing("PublicDataReader", "publicdatareader")
    _pip_install_if_missing("koreanize_matplotlib", "koreanize-matplotlib")

    # 기존 노트북들이 뒤 셀에서 쓰는 Ecos(한국은행 ECOS 클라이언트)를 전역에 주입
    try:
        from PublicDataReader import Ecos
        if namespace is not None:
            namespace["Ecos"] = Ecos
    except Exception as e:
        print(f"⚠️ PublicDataReader.Ecos 로드 실패: {e}")

    # --- 3) 스타일/표시 설정 (preamble_core) ---
    import preamble_core
    preamble_core.setup_notebook(save_dir=FIGS, seaborn_use=seaborn)
    if namespace is not None:
        preamble_core.bind_env(namespace)  # np/pd/mpl/plt/save_fig 등 주입

    import matplotlib.pyplot as plt
    plt.rcParams["figure.dpi"] = screen_dpi   # 화면 렌더링
    plt.rcParams["savefig.dpi"] = save_dpi    # 파일 저장

    # 한글 폰트
    try:
        import koreanize_matplotlib  # noqa: F401
    except Exception as e:
        print(f"⚠️ koreanize_matplotlib 로드 실패(한글이 깨질 수 있음): {e}")

    # 자주 쓰는 플로팅 함수 주입
    try:
        import plot_utils
        importlib.reload(plot_utils)
        if namespace is not None:
            namespace["plot_dual_axis"] = plot_utils.plot_dual_axis
    except Exception as e:
        print(f"⚠️ plot_utils 로드 실패: {e}")

    # --- 4) ECOS 키 ---
    key = _resolve_ecos_key(ecos_key)
    if key is None:
        msg = ("⚠️ ECOS API 키가 설정되지 않았습니다. "
               "Colab Secrets(🔑)에 'ECOS_API_KEY'를 저장하거나 "
               "init(ecos_key='...')로 넘기세요.")
        if require_ecos:
            print(msg)
            raise SystemExit
        else:
            print(msg + " (이 장은 ECOS 없이도 진행됩니다.)")
    if namespace is not None:
        namespace["key_api_ECOS"] = key  # 기존 노트북 변수명 호환

    # --- 5) NBER 침체구간 데이터 ---
    NBERm = NBERq = None
    if load_nber:
        try:
            import nber_utils
            if namespace is not None:
                nber_utils.bind_env(namespace)  # load_.../plot_nber_recession 주입
            local = os.path.join(root, "data", os.path.basename(NBER_LOCAL))
            source = NBER_URL if _looks_reachable(NBER_URL) else local
            NBERm, NBERq = nber_utils.load_and_process_nber_data(source)
            if namespace is not None:
                namespace["NBERm"] = NBERm
                namespace["NBERq"] = NBERq
        except Exception as e:
            print(f"⚠️ NBER 데이터 로딩 실패(이 장에서 침체음영을 못 쓸 수 있음): {e}")

    env = SimpleNamespace(
        ROOT=root, UTILS=UTILS, FIGS=FIGS, DATA=DATA,
        ecos_key=key, NBERm=NBERm, NBERq=NBERq,
    )
    print(f"✅ bootstrap 완료 · ROOT={root}")
    return env


def _looks_reachable(url, timeout=5):
    """URL이 실제로 열리는지 가볍게 확인(막히면 로컬 폴백 쓰도록)."""
    try:
        import urllib.request
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except Exception:
        return False
