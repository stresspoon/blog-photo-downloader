#!/usr/bin/env python3
"""
블로그 이미지 다운로더 빌드 스크립트
macOS에서 실행 가능한 .app 파일을 생성합니다.
"""

import subprocess
import sys
import os

def build_app():
    """PyInstaller를 사용하여 macOS .app 파일 빌드"""
    print("🚀 블로그 이미지 다운로더 빌드 시작...")
    
    # PyInstaller 명령어 구성 (selenium 의존성 완전 포함)
    cmd = [
        "pyinstaller",
        "--onedir",                               # 폴더로 빌드 (더 안정적)
        "--windowed",                             # GUI 모드
        "--name=BlogPhotoDownloader",             # 앱 이름
        "--strip",                                # 파일 크기 최적화
        "--clean",                                # 이전 빌드 정리
        
        # selenium 관련 모든 모듈 수집
        "--collect-all", "selenium",
        "--collect-all", "webdriver_manager",
        
        # 주요 selenium 모듈 명시적 포함
        "--hidden-import=selenium",
        "--hidden-import=selenium.webdriver",
        "--hidden-import=selenium.webdriver.chrome",
        "--hidden-import=selenium.webdriver.chrome.webdriver",
        "--hidden-import=selenium.webdriver.chrome.service",
        "--hidden-import=selenium.webdriver.common",
        "--hidden-import=selenium.webdriver.common.by",
        "--hidden-import=selenium.webdriver.chromium",
        "--hidden-import=selenium.webdriver.chromium.webdriver",
        
        # webdriver-manager 모듈 포함
        "--hidden-import=webdriver_manager",
        "--hidden-import=webdriver_manager.chrome", 
        "--hidden-import=webdriver_manager.utils",
        "--hidden-import=webdriver_manager.driver",
        "--hidden-import=webdriver_manager.core",
        "--hidden-import=webdriver_manager.core.utils",
        
        # 불필요한 대용량 모듈 제외
        "--exclude-module=matplotlib",
        "--exclude-module=numpy", 
        "--exclude-module=pandas",
        "--exclude-module=scipy",
        "--exclude-module=PIL",
        "--exclude-module=pytest",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
        
        "blog_photo_down.py"                      # 메인 스크립트
    ]
    
    try:
        print("📦 PyInstaller 실행 중...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 빌드 성공!")
        print(f"📁 빌드된 앱 위치: dist/BlogPhotoDownloader.app")
        
        # 앱 크기 확인
        app_path = "dist/BlogPhotoDownloader.app"
        if os.path.exists(app_path):
            size = get_folder_size(app_path)
            print(f"📊 앱 크기: {size:.1f} MB")
        
        print("\n🎉 빌드 완료! dist/BlogPhotoDownloader.app 파일을 실행해보세요.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        print(f"에러 출력: {e.stderr}")
        sys.exit(1)

def get_folder_size(folder_path):
    """폴더 크기 계산 (MB 단위)"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.exists(file_path):
                total_size += os.path.getsize(file_path)
    return total_size / (1024 * 1024)  # MB로 변환

if __name__ == "__main__":
    # Python 및 필수 패키지 확인
    print("🔍 환경 확인 중...")
    
    try:
        import PyInstaller
        print(f"✅ PyInstaller 버전: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller가 설치되어 있지 않습니다.")
        print("설치 명령: pip install pyinstaller")
        sys.exit(1)
    
    try:
        import selenium
        print(f"✅ Selenium 버전: {selenium.__version__}")
    except ImportError:
        print("❌ Selenium이 설치되어 있지 않습니다.")
        print("설치 명령: pip install -r requirements.txt")
        sys.exit(1)
    
    build_app() 