# -*- coding: utf-8 -*-
"""
normalize_notebooks.py — 노트북 JSON을 '리뷰 가능한' 정규 포맷으로 통일한다.

왜 필요한가?
- Colab은 노트북을 compact(전체 1줄) 형식으로 저장한다. 이 상태에서는 셀 하나만
  바뀌어도 git이 파일 전체를 바뀐 것으로 보고 diff가 사실상 불가능하다.
- 이 스크립트는 출력(그림 등)은 **그대로 유지**하면서 포맷만 indent=1로 정규화하여,
  이후 편집 시 '바뀐 셀만' diff되도록 만든다.
- 덤으로 Colab이 셀마다 심는 휘발성 메타데이터(실행 시각·저자 계정 정보 등)를 제거해
  diff 노이즈와 개인정보 노출을 줄인다.

사용법:
    python tools/normalize_notebooks.py                 # chapters/ + appendix_online/ 전체
    python tools/normalize_notebooks.py chapters/FE04_CAPM.ipynb   # 특정 파일만
    python tools/normalize_notebooks.py --check         # 변경 없이 정규화 필요 여부만 확인(CI용)
"""

import sys
import glob
import json
import os

# 셀 metadata에서 제거할 휘발성 키(실행마다 바뀌어 diff를 더럽힘)
VOLATILE_CELL_META = ("executionInfo", "outputId", "colab")
# 노트북 상단 metadata에서 제거할 키(위젯 상태 등 재현 불필요·거대)
VOLATILE_NB_META = ("widgets",)


def normalize_obj(nb):
    """nb(dict)를 제자리에서 정규화. 반환값은 동일 객체."""
    for key in VOLATILE_NB_META:
        nb.get("metadata", {}).pop(key, None)

    for cell in nb.get("cells", []):
        meta = cell.get("metadata", {})
        for key in VOLATILE_CELL_META:
            meta.pop(key, None)
        # 실행 카운트는 재현성과 무관하므로 비움(출력 자체는 유지)
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            for out in cell.get("outputs", []):
                if isinstance(out, dict):
                    out.pop("execution_count", None)
    return nb


def dumps_canonical(nb):
    """정규 직렬화: indent=1, 한글 유지, 키 순서 보존, 끝에 개행 1개."""
    return json.dumps(nb, ensure_ascii=False, indent=1) + "\n"


def process(path, check=False):
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    new = dumps_canonical(normalize_obj(nb))
    with open(path, encoding="utf-8") as f:
        old = f.read()
    if new == old:
        return False  # 이미 정규 상태
    if not check:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return True


def main(argv):
    check = "--check" in argv
    args = [a for a in argv if not a.startswith("--")]
    if args:
        targets = args
    else:
        targets = sorted(glob.glob("chapters/*.ipynb")) + \
                  sorted(glob.glob("appendix_online/*.ipynb"))
    changed = []
    for p in targets:
        if not os.path.exists(p):
            print(f"⚠️ 없음: {p}")
            continue
        if process(p, check=check):
            changed.append(p)
    verb = "정규화 필요" if check else "정규화됨"
    if changed:
        print(f"{verb} ({len(changed)}개):")
        for p in changed:
            print(f"  - {p}")
    else:
        print("✅ 모든 노트북이 이미 정규 포맷입니다.")
    # --check 모드에서 변경 필요가 있으면 비정상 종료(CI 게이트용)
    if check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
