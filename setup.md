# 설치 및 사용법

파이썬을 처음 접하는 독자도 쉽게 사용할 수 있도록 **Google Colab 사용을 권장**합니다.

## 0단계: 코드 살펴보기만 하는 경우

코드를 직접 실행하지 않고 코드와 결과물을 살펴보는 목적이라면:

```{admonition} GitHub에서 노트북 보기
:class: tip
1. [chapters 폴더](https://github.com/FinancialEconomicsPython/book/tree/main/chapters)로 이동
2. 보고 싶은 장의 `.ipynb` 파일 클릭
3. GitHub에서 코드와 결과를 바로 확인
```

💡 **실행 없이 결과만 확인하고 싶다면 여기까지만 하시면 됩니다!**

---

## 1단계: 실행 환경 준비

```{warning}
코드를 직접 실행하려면 반드시 먼저 수행해야 합니다!
```

### utils 폴더의 중요성

이 저장소의 대부분의 Jupyter Notebook은 `utils/` 폴더의 **공통 함수**를 사용합니다.

GitHub에서 노트북을 Google Colab으로 열 경우:
- 노트북 파일(`.ipynb`)만 복사됨
- **`utils/` 폴더는 자동으로 포함되지 않음**

따라서 아래 방법 중 하나를 선택하세요.

---

### ✅ 방법 A (권장): 저장소 전체 clone

가장 안정적인 방법입니다.

```python
# Colab 노트북 상단 셀에서 실행
!git clone https://github.com/FinancialEconomicsPython/book.git
%cd book
```

**장점:**
- utils/ 폴더 자동 포함
- 상대 경로 모두 정상 작동
- 저장소 업데이트 쉽게 반영

---

### ✅ 방법 B: utils 파일 수동 다운로드

1. [utils 폴더](https://github.com/FinancialEconomicsPython/book/tree/main/utils)로 이동
2. 다음 파일 다운로드:
   - `nber_utils.py`
   - `plot_utils.py`
   - `preamble_core.py`
3. Colab에서 `utils/` 폴더 생성 후 업로드

**최종 구조:**
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

### 방법 1: GitHub에서 Colab으로

1. [chapters 폴더](https://github.com/FinancialEconomicsPython/book/tree/main/chapters) 이동
2. 원하는 `.ipynb` 파일 클릭
3. BASE 경로와 ECOS API 키 설정
4. 셀을 위에서부터 실행 (`Shift + Enter`)

---

### 방법 2: Colab에서 직접

1. [Google Colab](https://colab.research.google.com) 접속
2. **파일 → 노트북 열기 → GitHub**
3. `FinancialEconomicsPython/book` 입력
4. 원하는 노트북 선택
5. 셀 실행

---

### 방법 3: 로컬 환경 (고급)

```bash
git clone https://github.com/FinancialEconomicsPython/book.git
cd book
jupyter notebook
```

```{warning}
파이썬 환경 설정에 익숙한 독자에게만 권장됩니다.
```

---

## ECOS API 키 발급

한국은행 데이터 사용을 위해 필요합니다.

1. [한국은행 ECOS](https://ecos.bok.or.kr/api/#/) 접속
2. 회원가입 후 로그인
3. API 신청 메뉴에서 인증키 발급
4. 노트북에서 사용:

```python
key_api_ECOS = "여기에_발급받은_키_입력"
```

---

## 문제 해결

### Q: ModuleNotFoundError: No module named 'utils'

**A:** 1단계의 방법 A 또는 B를 다시 확인하세요.

### Q: API 키 에러

**A:** `key_api_ECOS`에 실제 키를 입력했는지 확인하세요.

---

## 추가 도움

- 📧 Email: [financialeconomicspython@gmail.com](mailto:financialeconomicspython@gmail.com)
- 📚 [GitHub README](https://github.com/FinancialEconomicsPython/book/blob/main/README.md)
