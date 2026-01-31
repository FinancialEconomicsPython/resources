# -*- coding: utf-8 -*-
"""
preamble_core.py — General preamble for the '금융경제학' Colab notebooks.

특징
- save_fig: 모듈 전역 정의(바로 import 가능)
- setup_notebook: 표시/스타일/세이브 폴더 설정
- export_env / bind_env: Colab 셀 전역으로 안전하게 주입 (user_ns 이슈 해결)

사용 예 (노트북):
----------------
from google.colab import drive
drive.mount('/content/drive')

import sys
sys.path.append("/content/drive/MyDrive/Colab Notebooks/book_FinancialEconomics/utils")

from preamble_core import setup_notebook, bind_env, save_fig
FIGS = "/content/drive/MyDrive/Colab Notebooks/book_FinancialEconomics/figures"
setup_notebook(save_dir=FIGS, seaborn_use=True)
bind_env(globals())   # plt/np/pd/save_fig 등을 현재 셀 전역에 주입

# 저장이 되는지 확인
fig, ax = plt.subplots()
ax.plot(np.arange(10), np.sin(np.arange(10)))
save_fig("sanity_check")
"""

import os
import warnings
from datetime import date
from functools import reduce

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

try:
    import seaborn as sns
except Exception:
    sns = None

try:
    import pandas_datareader as pdr
except Exception:
    pdr = None

try:
    import scipy.optimize as solver
except Exception:
    solver = None

# -----------------------------
# 전역 저장 폴더 & save_fig
# -----------------------------
_DEFAULT_SAVE_DIR = None

def save_fig(fig_id, tight_layout=True, folder=None, dpi_override=None, fmt="png"):
    """현재 Matplotlib Figure를 지정 폴더에 저장."""
    target_dir = folder or _DEFAULT_SAVE_DIR
    if target_dir is None:
        raise ValueError("save_dir가 지정되지 않았습니다. setup_notebook(save_dir=...) 또는 save_fig(..., folder=...)로 지정하세요.")
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, f"{fig_id}.{fmt}")
    if tight_layout:
        plt.tight_layout()
    print(f"Saving figure → {path}")
    if dpi_override is None:
        plt.savefig(path, format=fmt, dpi=600)
    else:
        plt.savefig(path, format=fmt, dpi=dpi_override)


# -----------------------------
# 내부 헬퍼
# -----------------------------
def _set_retina(retina: bool = True):
    """Retina 인라인 백엔드 설정 (IPython이 없으면 무시)."""
    if not retina:
        return
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is not None:
            ip.run_line_magic("config", "InlineBackend.figure_format = 'retina'")
    except Exception:
        pass

def _apply_display_prefs(
    numpy_precision=3,
    numpy_suppress=True,
    pd_float_format="{:,.3f}".format,
    pd_max_rows=100,
    pd_max_cols=10,
    wide_repr=True,
):
    """numpy/pandas 표시 옵션 일괄 적용."""
    np.set_printoptions(precision=numpy_precision, suppress=numpy_suppress)
    pd.options.display.float_format = pd_float_format
    pd.options.display.max_rows = pd_max_rows
    pd.options.display.max_columns = pd_max_cols
    if wide_repr:
        pd.options.display.width = 0

def _apply_matplotlib_style(
    dpi=180,
    figsize=(8, 5),
    korean_unicode_minus=True,
    seaborn_use=False,
    seaborn_style="whitegrid",
    style_path=None,
):
    """matplotlib(+선택적 seaborn) 스타일 적용."""
    plt.rcParams["figure.figsize"] = figsize
    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams["savefig.dpi"] = dpi
    plt.rcParams["lines.linewidth"] = 2
    # plt.rcParams["lines.color"] = "b"  # 필요 시 주석 해제

    mpl.rcParams.update({
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    mpl.rc("axes", labelsize=12)
    mpl.rc("xtick", labelsize=12)
    mpl.rc("ytick", labelsize=12)
    mpl.rc("font", size=12)
    plt.rc("legend", fontsize=12)

    if korean_unicode_minus:
        plt.rcParams["axes.unicode_minus"] = False

    if style_path and os.path.exists(style_path):
        mpl.style.use(style_path)

    if seaborn_use and sns is not None:
        try:
            if hasattr(sns, "set_theme"):
                sns.set_theme()
            if seaborn_style:
                sns.set_style(seaborn_style)
        except Exception:
            pass


# -----------------------------
# 메인: 노트북 세팅
# -----------------------------
def setup_notebook(
    dpi=180,
    figsize=(8, 5),
    retina=True,
    korean_unicode_minus=True,
    numpy_precision=3,
    numpy_suppress=True,
    pd_float_format="{:,.3f}".format,
    pd_max_rows=100,
    pd_max_cols=10,
    wide_repr=True,
    seaborn_use=False,
    seaborn_style="whitegrid",
    style_path=None,
    save_dir=None,
):
    """노트북 환경 초기화 (표시/스타일/세이브 폴더)."""
    warnings.filterwarnings("ignore")

    _set_retina(retina=retina)
    _apply_display_prefs(
        numpy_precision=numpy_precision,
        numpy_suppress=numpy_suppress,
        pd_float_format=pd_float_format,
        pd_max_rows=pd_max_rows,
        pd_max_cols=pd_max_cols,
        wide_repr=wide_repr,
    )
    _apply_matplotlib_style(
        dpi=dpi,
        figsize=figsize,
        korean_unicode_minus=korean_unicode_minus,
        seaborn_use=seaborn_use,
        seaborn_style=seaborn_style,
        style_path=style_path,
    )

    # 기본 저장 폴더 등록
    global _DEFAULT_SAVE_DIR
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        _DEFAULT_SAVE_DIR = save_dir

    print("✅ Notebook environment initialized.")
    if _DEFAULT_SAVE_DIR:
        print(f"📂 Figures will be saved to: {_DEFAULT_SAVE_DIR}")


# -----------------------------
# 노트북 전역 주입 유틸 (Colab-safe)
# -----------------------------
def export_env():
    """노트북 셀 전역(globals)에 주입할 객체 묶음을 dict로 반환."""
    return dict(
        np=np, pd=pd, mpl=mpl, plt=plt,
        pdr=pdr, solver=solver, reduce=reduce, date=date,
        save_fig=save_fig
    )

def bind_env(ns):
    """원하는 네임스페이스(보통 globals())에 환경을 주입."""
    ns.update(export_env())
