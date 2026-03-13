# 금융경제학: 파이썬을 활용한 금융시장과 통화정책의 이해
**저자: 박기영 (연세대 경제학부)**

**출판사: 시그마프레스**

**출판연도: 2026**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

<img src="https://raw.githubusercontent.com/FinancialEconomicsPython/resources/main/data/CPI_joyplot.png" width="700">

---
이 저장소(repository)는 **『금융경제학: 파이썬을 활용한 금융시장과 통화정책의 이해』** 에 수록된 그림과 실증 분석을 **독자가 직접 재현(replicate)하고 확장**할 수 있도록 만든 파이썬 코드 모음입니다. 

이 저장소는 다음과 같은 용도로 활용될 수 있습니다:

- 학부 화폐금융론 수업
- 대학원 자산가격결정이론 및 매크로-파이낸스 수업
- 개인 프로젝트
- 실증 분석 연습 및 연구 아이디어 탐색

모두 자유롭게 수정·확장하여 사용하기를 권장합니다.

📌 책이나 코드에 있는 오류, 개선사항, 의견 등은 financialeconomicspython@gmail.com으로 보내 주세요. 고맙습니다. 

---
## 저장소 구조

```
FinancialEconomicsPython/book/
├── README.md              ← 저장소 메인 설명 (교재 안내, 사용법)
│ 
├── chapters/
│   └── 각 장(chapter)에서 사용된 그림과 분석을 재현할 수 있는 Jupyter Notebook (.ipynb)
│ 
├── readings/
│   └── 각 장의 논의와 관련된 뉴스 기사, 블로그 글, 보고서, 추가 읽을거리
│ 
├── appendix_online/
│   └── 온라인 부록
│ 
├── data/
│   └── 공유하는 데이터 파일. 
│ 
├── utils/                ← chapters 폴더에 있는 Jupyter Notebook에서 공통으로 사용하는 함수
│   ├── nber_utils.py
│   ├── plot_utils.py
│   └── preamble_core.py
│ 
└── correction_typo/
    └── 본문의 수정사항 및 오타
```

- **chapters/**  
  해당 장에 등장하는 주요 그림과 분석을 재현하는 `.ipynb` 파일을 포함하고 있습니다.

- **readings/**  
  각 장에서 다루는 주제와 관련된 신문 기사, 정책 보고서, 블로그 글, 참고할 만한 추가 읽을거리를 정리해 둔 폴더입니다.

- **appendix_online/**  
  책에서 다루지 않은 내용을 수록하고 있습니다.

- **data/**  
  API를 이용할 수 없는 경우 사용하는 데이터 파일을 모아 둔 폴더입니다. 5, 12, 18장과 부록의 코드 일부에서 사용됩니다.    

- **utils/**  
  데이터 불러오기, 그래프 그리기, 날짜 처리 등 여러 장에서 반복적으로 사용되는 코드를 모아 둔 폴더입니다.  
  독자는 이 폴더의 코드를 모두 이해하지 않아도 각 장의 노트북을 실행할 수 있습니다.

---
## 이 저장소를 사용하는 방법 (중요)

파이썬을 처음 접하는 독자도 쉽게 사용할 수 있도록 **Google Colab 사용을 권장**합니다.

대부분의 노트북은 다음과 같은 순서로 구성되어 있습니다.
1. 필요한 패키지 설치
2. 데이터 불러오기
3. 그림 및 실증 분석 재현

---

## 0단계: 코드를 살펴보기만 하는 경우

코드를 직접 실행하지 않고 코드와 결과물을 살펴보는 목적이라면:

### 🔹 GitHub에서 노트북 보기

1. 이 GitHub 저장소에서 [chapters/](https://github.com/FinancialEconomicsPython/resources/tree/main/chapters) 폴더로 이동합니다.
2. 보고 싶은 장의 ![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg) 을 클릭합니다. 
