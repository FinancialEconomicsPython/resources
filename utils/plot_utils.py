def plot_dual_axis(
    df, 
    left_vars, 
    right_vars=None, 
    vlines=None, 
    hlines=None,
    colors=None,
    linestyles=None,          # ✅ NEW: allow user-specified linestyles
    title=None,
    left_label="(%)", 
    right_label=None,
    figsize=(8, 4), 
    linewidth=1.5, 
    legend_loc="lower right",
    color_mode="default",     # "default" | "bw" | "limited"
    show_legend=True,         # legend 표시 여부
    legend_labels=None,       # 범례 이름 지정 (left/right 구분 없이 순서대로)
    legend_fontsize=11,       # legend 폰트 크기
    legend_ncol=1,            # legend 열(column) 수
    # ✅ 새 옵션
    y_left_format=None,       # 예: '{x:,.0f}'
    y_right_format=None,      # 예: '{x:,.1f}'
    left_label_rotation=90,
    right_label_rotation=90,
    save=None,                
    save_dpi=600,
    return_axes=False, 
    show=True
):
    """
    hlines 형식(둘 다 지원, 하위호환 유지):
      1) 전체폭: (y, label, color[, axis])
         - axis 생략/left/right
      2) 구간지정: (y, label, color[, axis], xmin, xmax[, linestyle='--'[, linewidth=1.0[, alpha=1.0]]])
         - axis 생략 시 'left'로 가정

    linestyles:
      - None이면: color_mode=="bw"일 때만 ["-","--","-. ",":"]를 순환 적용,
                 그 외에는 모두 실선("-")
      - 리스트/튜플로 주면: left_vars + right_vars 순서대로 적용(길이 부족하면 순환)
        예) linestyles=['-','--','-.',':']
    """

    import matplotlib.pyplot as plt
    import pandas as pd
    import matplotlib as mpl
    from matplotlib import cm

    # 🔧 PeriodIndex → DatetimeIndex 자동 변환
    if isinstance(df.index, pd.PeriodIndex):
        df = df.copy()
        df.index = df.index.to_timestamp(how='end')  # 필요 시 'start'

    # --- ① 팔레트 정의 ---
    if colors is not None:
        palette = list(colors)
    else:
        if color_mode == "bw":
            palette = ["black", "dimgray", "gray"]
        elif color_mode == "limited":
            palette = ["black", "#555555", "#004488"]
        else:  # default
            palette = [cm.tab10(i) for i in range(10)]

    # --- ①-2 선스타일 정의 (✅ 사용자가 주면 최우선) ---
    if linestyles is not None:
        linestyles = list(linestyles)
        if len(linestyles) == 0:
            linestyles = ["-"]
    else:
        if color_mode == "bw":
            linestyles = ["-", "--", "-.", ":"]
        else:
            linestyles = ["-"]

    # --- ② 색/스타일 선택 함수 ---
    # idx는 (left_vars + right_vars) 전체에서의 순번
    def get_style(idx: int):
        color = palette[idx % len(palette)]
        style = linestyles[idx % len(linestyles)]
        return color, style

    # --- ③ Figure / Axes ---
    fig, ax1 = plt.subplots(figsize=figsize)

    # --- ④ 왼쪽 축 ---
    for i, col in enumerate(left_vars):
        color, style = get_style(i)
        label = legend_labels[i] if (legend_labels and i < len(legend_labels)) else col
        ax1.plot(
            df.index, df[col],
            label=label,
            color=color,
            linestyle=style,
            linewidth=linewidth
        )
    ax1.set_ylabel(left_label, rotation=left_label_rotation)
    ax1.grid(True, alpha=0.3)
    if y_left_format:
        ax1.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter(y_left_format))

    # --- ⑤ 오른쪽 축 ---
    ax2 = None
    if right_vars:
        ax2 = ax1.twinx()
        for j, col in enumerate(right_vars):
            idx = len(left_vars) + j
            color, style = get_style(idx)
            label_idx = len(left_vars) + j
            label = (
                legend_labels[label_idx]
                if (legend_labels and label_idx < len(legend_labels))
                else col
            )
            ax2.plot(
                df.index, df[col],
                label=label,
                color=color,
                linestyle=style,
                linewidth=linewidth
            )

        if right_label:
            ax2.set_ylabel(right_label, rotation=right_label_rotation)
        if y_right_format:
            ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter(y_right_format))

    # --- ⑥ 범례 표시 ---
    if show_legend:
        if right_vars:
            lines_1, labels_1 = ax1.get_legend_handles_labels()
            lines_2, labels_2 = ax2.get_legend_handles_labels()
            ax1.legend(
                lines_1 + lines_2, labels_1 + labels_2,
                loc=legend_loc, fontsize=legend_fontsize, ncol=legend_ncol
            )
        else:
            ax1.legend(loc=legend_loc, fontsize=legend_fontsize, ncol=legend_ncol)

    # --- ⑦ 수직선 ---
    if vlines:
        for v in vlines:
            # 기존: (x, label, color)
            # 확장: (x, label, color[, linestyle='--'[, linewidth=1[, label_pos='right'[, label_ypos=0.9]]]])
            x, label, color = v[0], v[1], v[2]
            linestyle_v = v[3] if len(v) > 3 else '--'
            linewidth_v = v[4] if len(v) > 4 else 1.0
            label_pos = v[5] if len(v) > 5 else 'right'   # 'left' | 'right' | 'center' | None
            label_ypos = v[6] if len(v) > 6 else 0.9       # 0~1 사이, 높이 비율

            xdt = pd.to_datetime(x)
            ax1.axvline(x=xdt, color=color, linestyle=linestyle_v, linewidth=linewidth_v, label='_nolegend_')

            # 라벨 표시
            if label:
                if label_pos == 'left':
                    ha = 'right'
                elif label_pos == 'center':
                    ha = 'center'
                else:  # right
                    ha = 'left'

                ax1.text(
                    xdt, label_ypos, label,
                    color=color, fontsize=11,
                    ha=ha, va='center',
                    rotation=0,
                    transform=ax1.get_xaxis_transform()
                )

    # --- ⑧ 수평선 (하위호환 + 구간 확장) ---
    if hlines:
        for h in hlines:
            # 기본 파싱
            if len(h) in (3, 4):
                # 전체폭: (y, label, color[, axis])
                y, label, color = h[0], h[1], h[2]
                axis = h[3] if len(h) == 4 else "left"
                target_ax = ax1 if (axis == "left" or ax2 is None) else ax2
                target_ax.axhline(y=y, color=color, linestyle='--', linewidth=1, label='_nolegend_')

                xmin, xmax = df.index.min(), df.index.max()
                if label:
                    xpad = (xmax - xmin) * 0.02
                    xpos = xmin + xpad
                    target_ax.text(
                        xpos, y, label, color=color,
                        va='bottom', ha='left', fontsize=11, rotation=0,
                        clip_on=True
                    )
            else:
                # 구간지정: (y, label, color[, axis], xmin, xmax[, linestyle='--'[, linewidth=1.0[, alpha=1.0]]])
                y, label, color = h[0], h[1], h[2]
                idx = 3
                axis = "left"
                if isinstance(h[idx], str) and h[idx] in ("left", "right"):
                    axis = h[idx]
                    idx += 1
                xmin, xmax = h[idx], h[idx+1]
                idx += 2
                linestyle_h = h[idx] if len(h) > idx else '--'
                linewidth_h = h[idx+1] if len(h) > idx+1 else 1.0
                alpha = h[idx+2] if len(h) > idx+2 else 1.0

                target_ax = ax1 if (axis == "left" or ax2 is None) else ax2
                target_ax.hlines(
                    y=y, xmin=xmin, xmax=xmax, colors=color,
                    linestyles=linestyle_h, linewidth=linewidth_h, alpha=alpha
                )
                if label:
                    target_ax.text(
                        xmin, y, f" {label}", color=color,
                        va='bottom', ha='left', fontsize=11, rotation=0
                    )

    if title:
        ax1.set_title(title)

    plt.tight_layout()

    # --- ⑨ 저장 옵션 ---
    if isinstance(save, str) and save.strip():
        if "save_fig" in globals() and callable(globals()["save_fig"]):
            globals()["save_fig"](save)
        else:
            plt.savefig(f"{save}.png", dpi=save_dpi, bbox_inches="tight")

    if return_axes:
        return fig, ax1, ax2
    if show:
        plt.show()
