# 블로그 포토 다운로더

웹페이지에서 모든 이미지를 자동으로 다운로드하는 GUI 프로그램입니다.

## 🌟 주요 기능

- 웹페이지의 모든 이미지 자동 검색 및 다운로드
- iframe 내부 이미지도 검색
- 배경 이미지(CSS background-image)도 다운로드
- 사용자 친화적인 GUI 인터페이스
- 실시간 다운로드 로그 표시
- 중복 파일명 자동 처리

## 📋 요구사항

- Python 3.7+
- Chrome 브라우저 설치 필수
- 인터넷 연결

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Python으로 직접 실행
```bash
python blog_photo_down.py
```

### 3. exe 파일로 빌드하기

#### 자동 빌드 (권장)
```bash
python build.py
```

#### 수동 빌드 (최적화된 버전)
```bash
# PyInstaller 설치
pip install pyinstaller

# UPX 설치 (macOS)
brew install upx

# 최적화된 앱 생성 (크기 최적화)
pyinstaller --onedir --windowed --name=BlogPhotoDownloader \
    --strip --clean \
    --hidden-import=webdriver_manager.chrome \
    --hidden-import=selenium.webdriver.chrome.service \
    --exclude-module=matplotlib --exclude-module=numpy \
    --exclude-module=pandas --exclude-module=scipy \
    --exclude-module=PIL --exclude-module=pytest \
    --exclude-module=IPython --exclude-module=jupyter \
    blog_photo_down.py
```

## 📂 빌드 결과

빌드가 완료되면 다음 구조로 파일이 생성됩니다:
```
blog_photo/
├── dist/
│   └── BlogPhotoDownloader.app  # 실행 파일 (41MB - 최적화됨)
├── build/                       # 임시 빌드 파일 (삭제 가능)
└── BlogPhotoDownloader.spec     # PyInstaller 설정 (삭제 가능)
```

### 🚀 크기 최적화 결과
- **기본 빌드**: 286MB
- **최적화 빌드**: 41MB (85% 크기 감소!)
- **최적화 적용 사항**:
  - 불필요한 모듈 제외 (matplotlib, numpy, pandas 등)
  - 디버그 심볼 제거 (--strip)
  - UPX 압축 준비

## 💻 사용법

1. **URL 입력**: 다운로드할 웹페이지 URL 입력
2. **폴더 선택**: 이미지를 저장할 폴더 선택
3. **다운로드 시작**: 버튼 클릭으로 자동 다운로드 시작
4. **로그 확인**: 실시간으로 다운로드 진행상황 확인

## 🔧 지원 파일 형식

- JPG/JPEG
- PNG
- GIF
- WebP

## ⚠️ 주의사항

- Chrome 브라우저가 반드시 설치되어 있어야 합니다
- 일부 웹사이트는 봇 접근을 차단할 수 있습니다
- 대용량 이미지나 많은 이미지가 있는 페이지는 시간이 오래 걸릴 수 있습니다
- 저작권이 있는 이미지의 경우 사용에 주의하세요

## 🎯 성능 최적화

### 크기 최적화
- 기본 빌드 대비 **85% 크기 감소** (286MB → 41MB)
- 불필요한 과학 계산 라이브러리 제거
- 디버그 심볼 스트리핑 적용

### 실행 속도
- 최적화된 빌드는 앱 시작 시간이 더 빠름
- 메모리 사용량 감소
- 기능상 차이 없음

## 🐛 문제 해결

### exe 파일이 실행되지 않는 경우
1. Chrome 브라우저 설치 확인
2. 백신 프로그램에서 예외 처리
3. 관리자 권한으로 실행

### 다운로드가 되지 않는 경우
1. 인터넷 연결 확인
2. 웹페이지 접근 가능 여부 확인
3. URL 형식 확인 (http:// 또는 https://)

## 📝 라이선스

이 프로젝트는 개인적 용도로 자유롭게 사용할 수 있습니다. 