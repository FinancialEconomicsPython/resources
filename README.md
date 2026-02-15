# 금융경제학: 파이썬을 활용한 금융시장과 통화정책의 이해
**저자: 박기영 (연세대 경제학부)**

**출판사: 시그마프레스**

**출판연도: 2026**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)


---

이 저장소(repository)는 **『금융경제학: 파이썬을 활용한 금융시장과 통화정책의 이해』** 에 수록된 그림과 실증 분석을 **독자가 직접 재현(replicate)하고 확장**할 수 있도록 만든 파이썬 코드 모음입니다. 

이 저장소의 목적은 단순히 책 속의 결과를 다시 확인하는데 있지 않습니다. 독자들이 **데이터의 표본기간을 바꾸고**, **변수를 추가·제거하고**, **분석 가정을 수정**하면서 금융경제학적 직관을 스스로 형성하는 데 도움을 주는 것을 목표로 합니다.

이 저장소는 다음과 같은 용도로 활용될 수 있습니다.

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

1. 이 GitHub 저장소에서 `chapters/` 폴더로 이동합니다.
2. 보고 싶은 장의 `.ipynb` 파일을 클릭합니다.
3. GitHub에서 노트북의 코드와 결과를 바로 볼 수 있습니다.

💡 **실행 없이 결과만 확인하고 싶다면 여기까지만 하시면 됩니다!**

---

## 1단계: 실행 환경 준비 (⚠️ 코드를 직접 실행하려면 반드시 먼저 수행)

> ⚠️ **IMPORTANT — `utils/` 폴더 관련 공통 안내**

이 저장소의 대부분의 Jupyter Notebook은  
`utils/` 폴더에 포함된 **공통 함수**를 사용합니다  
(그래프 작성, 데이터 처리, 날짜 처리 등).

GitHub에서 노트북을 **Google Colab**으로 열 경우,

- 노트북 파일(`.ipynb`) **만** Colab 환경으로 복사되며
- **`utils/` 폴더는 자동으로 포함되지 않습니다.**

따라서 노트북을 실행하기 전에,  
아래의 **방법 A 또는 방법 B 중 하나를 반드시 선택**하여  
`utils/` 폴더를 작업 환경에 포함시켜 주십시오.

---

### ✅ 방법 A (권장): 저장소 전체를 Colab 환경에 clone 하기

가장 안정적인 방법이며,  
모든 노트북이 **저자 의도대로 동일하게 동작**합니다.

#### 노트북 상단 셀에서 아래 코드 실행
```python
# FinancialEconomicsPython 저장소를 Colab 환경으로 복제
!git clone https://github.com/FinancialEconomicsPython/book.git

# 작업 디렉토리를 저장소 루트로 이동
%cd book
```
이 방법을 사용하면 utils/ 폴더가 자동으로 포함되고
chapters/, readings/ 등 상대경로가 모두 정상 작동하며
저장소 업데이트 내용도 쉽게 반영할 수 있습니다.

### ✅ 방법 B: utils 폴더의 파일을 다운로드 받기

1. 이 저장소의 utils/ 폴더로 이동합니다.
2. 다음 파일들이 있는지 확인합니다.
    nber_utils.py
    plot_utils.py
    preamble_core.py
3. 파일을 다운로드합니다.
4. 작업 폴더에 utils/라는 이름의 폴더를 생성하고 파일을 업로드 합니다. 
👉 최종적으로 Colab의 파일 구조가 아래와 같아야 합니다.

```
/content/
├── your_notebook.ipynb
└── utils/
    ├── nber_utils.py
    ├── plot_utils.py
    └── preamble_core.py
```

--- 
## 2단계: 노트북 실행하기

### 🔹 방법 1: GitHub에서 Colab으로 열기
1. 이 GitHub 저장소에서 `chapters/` 폴더로 이동합니다.
2. 실행하고 싶은 장의 `.ipynb` 파일을 클릭합니다.
3. 해당 파일의 첫 부분에 나와 있는 설명대로 본인이 작업할 폴더 경로 BASE, 그리고 한국은행 ECOS API 인증키를 key_api_ECOS에 지정해 줍니다.
4. 노트북의 셀(cell)을 **위에서부터 차례대로 실행**합니다.
- 단축키: `Shift + Enter`

### 🔹 방법 2: Google Colab에서 직접 열기
1. Google Colab에 접속합니다.  
   https://colab.research.google.com
2. 상단 메뉴에서  
   **파일 → 노트북 열기 → GitHub** 를 선택합니다.
3. 저장소 이름(`FinancialEconomicsPython/book`) 또는  
   실행하고 싶은 노트북의 GitHub URL을 입력합니다.
4. 목록에서 원하는 `.ipynb` 파일을 선택하여 엽니다.
5. 노트북의 셀(cell)을 **위에서부터 차례대로 실행**합니다.
- 단축키: `Shift + Enter`

### 🔹 방법 3: 파일을 다운로드하여 직접 실행하기 (고급 사용자)

로컬 환경에서 파이썬을 사용하는 독자는 다음과 같이 사용할 수 있습니다.

1. 이 저장소를 `git clone` 하거나 ZIP 파일로 다운로드합니다.
2. Jupyter Notebook 또는 JupyterLab에서 `.ipynb` 파일을 실행합니다.
3. `utils/` 폴더가 같은 디렉토리에 있어야 합니다.

⚠️ 이 방법은 파이썬 환경 설정에 익숙한 독자에게만 권장됩니다.

---
## License

This repository is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You are free to use, modify, and redistribute the code and figures in this repository
for research, teaching, and other purposes, provided that appropriate credit is given.


### Citation (Required)

If you use or adapt this code, please cite the following book:

Park, Ki Young (2026),  
*Financial Economics: Analyzing Financial Markets and Monetary Policy with Python*,  
Sigma Press.  

GitHub repository: https://github.com/FinancialEconomicsPython/book


## 라이선스 안내 (한글)

본 저장소에 포함된 모든 코드는 **크리에이티브 커먼즈 저작자표시 4.0 국제 라이선스(CC BY 4.0)** 하에 공개됩니다.

연구, 강의, 보고서, 출판물 등 다양한 목적으로 자유롭게 사용·수정·재배포할 수 있으나, 아래의 인용 표기를 반드시 포함해 주시기 바랍니다.


### 인용 방법 (필수)

본 저장소의 코드를 사용하거나 수정하여 활용한 경우,  
다음 문헌을 반드시 인용해 주십시오.

박기영 (2026),  
『금융경제학: 파이썬을 활용한 금융시장과 통화정책의 이해』,  
시그마프레스.

GitHub 저장소: https://github.com/FinancialEconomicsPython/book



---

### Note on Data Sources

Data used in this repository (e.g., FRED, ECOS, ECB Data Portal) are subject to their own licenses.
This license applies only to the original code and figures created by the author.
