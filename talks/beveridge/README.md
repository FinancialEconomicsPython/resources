# 베버리지 곡선: 미국 노동시장은 얼마나 뜨거운가?

<a href="https://colab.research.google.com/github/FinancialEconomicsPython/resources/blob/main/talks/beveridge/beveridge_curve.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

미국의 실업률과 빈일자리율로 베버리지 곡선을 그리고, 표본기간과 시기 구분을 바꿔 가며 직접 분석해 보는 노트북입니다.
『금융경제학: 파이썬을 활용한 금융시장과 통화정책의 이해』(박기영, 시그마프레스) 18장의 분석을 발표용으로 정리했습니다.

- 데이터: 미국 세인트루이스 연준 **FRED** (API 키 불필요)
- 그림: ① 실업률·빈일자리율 추이 ② 시기별 베버리지 곡선 ③ 시간 흐름에 따른 베버리지 곡선 ④ 노동시장 과열도(V/U 비율)

## 실행 방법 (3단계)

1. 위의 **Open in Colab** 버튼을 누르고, 화면 오른쪽 위에서 Google 계정으로 **로그인** 합니다.
2. 위쪽 메뉴 **런타임 → 모두 실행** 을 누릅니다. "Google에서 작성하지 않은 노트북" 경고가 뜨면 **무시하고 계속하기** 를 누르세요.
   (이 노트북은 공개 데이터를 내려받아 그림만 그리며, 내 Google 드라이브나 개인정보에 접근하지 않습니다.)
3. **② 분석 설정** 칸에서 기간을 바꾸고 다시 **런타임 → 모두 실행** 을 누릅니다.

수정한 내용을 보관하려면 **파일 → Drive에 사본 저장** 을 누르세요. 내 드라이브에 복사본이 생기고 원본은 바뀌지 않습니다.

## 발표별 링크

발표 당일의 내용 그대로 고정된 링크입니다. (태그는 발표 직전에 만듭니다.)

| 발표 | 링크 |
|---|---|
| 신영증권 (2026년 10월) | [Colab에서 열기](https://colab.research.google.com/github/FinancialEconomicsPython/resources/blob/talk-2026-10-shinyoung/talks/beveridge/beveridge_curve.ipynb) |
| 한국은행 출입기자 간담회 (2026년 11월) | [Colab에서 열기](https://colab.research.google.com/github/FinancialEconomicsPython/resources/blob/talk-2026-11-bok-press/talks/beveridge/beveridge_curve.ipynb) |

## 파일

| 파일 | 내용 |
|---|---|
| `beveridge_curve.ipynb` | 노트북 본체 |
| `beveridge_snapshot.csv` | FRED 데이터 사본 (2000.12~). FRED 접속이 안 되면 노트북이 자동으로 이 파일을 씁니다. |

## 내 컴퓨터에서 실행하기

Colab이 막힌 환경이라면 `beveridge_curve.ipynb` 와 `beveridge_snapshot.csv` 를 같은 폴더에 내려받아 Jupyter에서 실행하면 됩니다.
필요한 패키지는 `pandas`, `numpy`, `matplotlib` 뿐이며, 한글 글꼴은 Windows(맑은 고딕)·Mac(AppleGothic)의 기본 글꼴을 자동으로 사용합니다.
