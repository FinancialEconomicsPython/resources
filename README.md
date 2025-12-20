# 금융경제학: 파이썬을 활용한 금융시장과 통화정책의 이해
## 1. 이 책에 대하여



## 2. 관련 기사, 블로그 등

### 3. 파이썬 활용하기 



utils 폴더 안내
이 폴더에는 책 전체(chapters 전반)에서 공통으로 사용하는 파이썬 유틸리티 코드를 모아 두었습니다.
각 장(chapters/)에서는 개별 분석과 그림 생성에 집중하고, 반복적으로 쓰이는 설정·그래프·외부 데이터 처리는 이 폴더의 함수들을 불러와 사용합니다.
1️⃣ preamble_core.py
노트북 환경과 그림 스타일을 통일하는 초기 설정 파일
역할
각 장 노트북에서 반복되는 그래프 스타일, 표시 옵션, 저장 규칙을 한 번에 설정
그림의 해상도, 폰트, 색상, 저장 경로 등을 책 전체에서 일관되게 유지
주요 기능
setup_notebook(...)
: 노트북 환경 초기화(스타일, dpi, 저장 경로 등)
save_fig(name, ...)
: 그림을 정해진 규칙으로 저장
export_env(), bind_env(ns)
: Colab/노트북에서 유틸 함수를 전역으로 쉽게 불러오기 위한 편의 함수
사용 라이브러리
표준 라이브러리: os, warnings, datetime, functools
데이터/수치: numpy, pandas
시각화: matplotlib (pyplot, dates, rcParams 등)
2️⃣ plot_utils.py
책 전반에서 사용하는 표준 시계열 그래프 함수 모음
역할
좌·우 이중축(dual-axis) 시계열 그래프를 한 함수로 표준화
장마다 반복되는 plotting 코드를 줄이고, 일관된 그림 형식을 제공
주요 기능
plot_dual_axis(...)
왼쪽/오른쪽 축에 여러 시계열을 동시에 그림
범례, 축 포맷, 선 스타일, 기준선(vlines/hlines) 옵션 지원
linestyles=[...] 인자를 통해 선 스타일을 처음부터 명시적으로 지정
→ 실제 선과 legend가 항상 일치하도록 설계
사용 라이브러리
데이터: pandas
시각화: matplotlib.pyplot, matplotlib.cm, matplotlib.ticker
3️⃣ nber_utils.py
NBER 경기침체(recession) 데이터 처리 및 음영 표시 유틸
역할
NBER Business Cycle Dating Committee의 공식 엑셀 자료를 불러와
**경기침체 구간(peak–trough)**을 정리
시계열 그래프 위에 **경기침체 음영(shading)**을 손쉽게 추가
주요 기능
load_and_process_nber_data(url)
NBER 엑셀 파일을 읽어
월별(NBERm)·분기별(NBERq) recession 구간 데이터 생성
plot_nber_recession(ax, nber_df, ...)
지정한 Axes에 경기침체 기간을 음영 처리
현재 x축 범위 밖의 과거 구간은 자동으로 제외되도록 설계
export_env(), bind_env(ns)
다른 장 노트북에서 쉽게 불러오기 위한 보조 함수
사용 라이브러리
표준 라이브러리: re (문자열/날짜 파싱)
데이터/입출력: pandas (read_excel, PeriodIndex)
시각화: matplotlib.pyplot
📌 정리
chapters/: 각 장에서 실제로 사용하는 분석·그림 코드
utils/: 모든 장에서 공통으로 사용하는 설정, 그래프, 외부 데이터 처리 코드
