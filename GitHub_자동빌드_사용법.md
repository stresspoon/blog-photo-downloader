# GitHub Actions로 윈도우/맥 exe 파일 자동 생성하기

## 🚀 **사용 방법**

### 1. GitHub 계정 생성 및 레포지토리 생성
1. https://github.com 에서 계정 생성
2. "New repository" 클릭
3. 레포지토리 이름: `blog-photo-downloader`
4. Public으로 설정 (Private도 가능)

### 2. 파일 업로드
다음 파일들을 GitHub 레포지토리에 업로드:
```
📁 blog-photo-downloader/
├── blog_photo_down.py
├── requirements.txt
├── build.py
├── README.md
└── .github/
    └── workflows/
        └── build.yml
```

### 3. 자동 빌드 실행
- 파일 업로드하면 **자동으로 빌드 시작**
- 또는 **Actions 탭** → **Build Cross-Platform Apps** → **Run workflow** 클릭

### 4. 생성된 파일 다운로드
빌드 완료 후 (약 5-10분):
1. **Actions 탭** 클릭
2. 가장 최근 빌드 클릭
3. **Artifacts** 섹션에서 다운로드:
   - `BlogPhotoDownloader-Windows.exe` (윈도우용)
   - `BlogPhotoDownloader-macOS.zip` (맥용)
   - `BlogPhotoDownloader-Linux` (리눅스용)

## 📦 **생성되는 파일들**

### Windows
- `BlogPhotoDownloader-Windows.exe` (단일 실행 파일)
- 크기: 약 20-30MB
- 윈도우 7/10/11 지원

### macOS  
- `BlogPhotoDownloader-macOS.app` (앱 번들)
- 크기: 약 40MB
- Intel/Apple Silicon 모두 지원

### Linux
- `BlogPhotoDownloader-Linux` (실행 파일)
- 크기: 약 30MB  
- Ubuntu/Debian 계열 지원

## ⚡ **장점**
- ✅ **무료**로 모든 플랫폼용 실행 파일 생성
- ✅ **자동화**: 코드 수정하면 자동으로 새 버전 빌드
- ✅ **클라우드**: 내 컴퓨터 자원 사용 안 함
- ✅ **배포**: GitHub Releases로 쉬운 배포

## 🔄 **업데이트 방법**
1. 코드 수정
2. GitHub에 업로드  
3. 자동으로 새 버전 빌드됨
4. Artifacts에서 새 파일 다운로드

---
💡 **GitHub을 사용하지 않으려면**: 윈도우 PC에서 직접 빌드하거나, Docker/Wine 사용 