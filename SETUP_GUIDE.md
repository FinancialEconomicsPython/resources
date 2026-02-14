# GitHub Pages 설정 가이드

이 문서는 Jupyter Book 기반 GitHub Pages를 실제 저장소에 적용하는 방법을 설명합니다.

## 📋 필요한 파일들

다음 파일들을 GitHub 저장소의 **루트 디렉토리**에 추가해야 합니다:

```
FinancialEconomicsPython/book/
├── _config.yml              ← Jupyter Book 설정
├── _toc.yml                 ← 목차 구조
├── intro.md                 ← 홈페이지
├── setup.md                 ← 설치 가이드
├── license.md               ← 라이선스
├── requirements.txt         ← Python 패키지
├── references.bib           ← 참고문헌
│
├── .github/
│   └── workflows/
│       └── deploy.yml       ← 자동 배포 설정
│
├── chapters/
│   └── README.md            ← (기존 노트북들과 함께)
│
├── readings/
│   └── README.md
│
└── appendix_online/
    └── README.md
```

---

## 🚀 설정 단계

### 1단계: 파일 업로드

1. 이 폴더의 모든 파일을 GitHub 저장소에 업로드합니다
2. 기존 README.md는 유지하거나 intro.md로 대체할 수 있습니다

### 2단계: GitHub Pages 활성화

1. GitHub 저장소 페이지로 이동
2. **Settings** → **Pages** 클릭
3. **Source** 섹션에서:
   - **Source**: `GitHub Actions` 선택
4. 저장

### 3단계: 첫 배포

1. main 브랜치에 파일을 커밋하면 자동으로 빌드가 시작됩니다
2. **Actions** 탭에서 진행 상황 확인
3. 빌드 완료 후 `https://financialeconomicspython.github.io/book/` 에서 확인

---

## ⚙️ 주요 파일 설명

### `_config.yml`
- 사이트 제목, 저자, 테마 등 기본 설정
- 저장소 URL과 라이선스 정보

### `_toc.yml`
- 사이트 네비게이션 구조
- 챕터와 섹션 순서

### `.github/workflows/deploy.yml`
- GitHub Actions 자동 배포 스크립트
- main 브랜치에 push할 때마다 자동 실행

---

## 🔧 커스터마이징

### 로고 추가
1. 로고 이미지를 저장소에 업로드 (예: `logo.png`)
2. `_config.yml`에서 수정:
```yaml
logo: logo.png
```

### 테마 색상 변경
`_config.yml`의 `sphinx.config` 섹션에서 테마 옵션 추가:
```yaml
html_theme_options:
  primary_color: "#0066cc"
```

### 목차 구조 변경
`_toc.yml` 파일을 수정하여 챕터 순서나 구조 변경

---

## 📝 업데이트 방법

### 내용 업데이트
1. `.md` 파일이나 `.ipynb` 파일 수정
2. GitHub에 커밋 & 푸시
3. 자동으로 재빌드 및 배포

### 새 챕터 추가
1. `chapters/` 폴더에 새 노트북 추가
2. `_toc.yml`에 추가 (또는 `glob` 패턴 사용)
3. 커밋 & 푸시

---

## ❓ 문제 해결

### 빌드 실패
- **Actions** 탭에서 에러 로그 확인
- 대부분 `.yml` 파일의 들여쓰기 문제

### 페이지가 업데이트되지 않음
- GitHub Actions가 완료되었는지 확인 (5-10분 소요)
- 브라우저 캐시 삭제 후 재시도

### 한글이 깨짐
- `_config.yml`에 `language: ko` 설정 확인

---

## 🔗 참고 자료

- [Jupyter Book 공식 문서](https://jupyterbook.org/)
- [GitHub Pages 문서](https://docs.github.com/en/pages)
- [GitHub Actions 문서](https://docs.github.com/en/actions)

---

## 📧 문의

설정 과정에서 문제가 발생하면 [financialeconomicspython@gmail.com](mailto:financialeconomicspython@gmail.com)으로 문의하세요.
