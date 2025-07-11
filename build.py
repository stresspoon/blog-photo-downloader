#!/usr/bin/env python3
"""
blog_photo_down.py를 exe 파일로 빌드하는 스크립트
"""

import os
import subprocess
import sys

def build_exe():
    """PyInstaller를 사용하여 exe 파일 생성"""
    
    print("🔧 블로그 포토 다운로더 빌드 시작...")
    
    # PyInstaller 명령어 구성 (UPX 최적화 포함)
    command = [
        "pyinstaller",
        "--onedir",  # 폴더로 생성 (macOS에서 권장)
        "--windowed",  # 콘솔 창 숨기기 (GUI 애플리케이션)
        "--name=BlogPhotoDownloader",  # 앱 파일명
        "--upx-dir=/opt/homebrew/bin",  # UPX 압축 사용
        "--strip",  # 디버그 심볼 제거
        "--clean",  # 이전 빌드 파일 정리
        "--hidden-import=webdriver_manager.chrome",
        "--hidden-import=selenium.webdriver.chrome.service",
        # 불필요한 모듈들 제외하여 크기 최적화
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--exclude-module=scipy",
        "--exclude-module=PIL",
        "--exclude-module=pytest",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",
        "blog_photo_down.py"
    ]
    
    try:
        # 빌드 실행
        print("📦 PyInstaller 실행 중...")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print("✅ 빌드 성공!")
        print(f"📁 생성된 앱: dist/BlogPhotoDownloader.app (macOS)")
        print("\n🎉 빌드 완료! dist 폴더에서 앱 파일을 확인하세요.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller가 설치되어 있지 않습니다.")
        print("다음 명령어로 설치하세요: pip install pyinstaller")
        return False
    
    return True

def clean_build():
    """빌드 파일들 정리"""
    import shutil
    
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["BlogPhotoDownloader.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"🧹 {dir_name} 폴더 삭제...")
            shutil.rmtree(dir_name)
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            print(f"🧹 {file_name} 파일 삭제...")
            os.remove(file_name)

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 블로그 포토 다운로더 빌드 도구")
    print("=" * 50)
    
    # 필요한 패키지 확인
    try:
        import PyInstaller
        print("✅ PyInstaller 설치됨")
    except ImportError:
        print("❌ PyInstaller가 설치되어 있지 않습니다.")
        print("설치하시겠습니까? (y/n): ", end="")
        response = input().lower()
        if response == 'y':
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        else:
            print("PyInstaller가 필요합니다. 종료합니다.")
            sys.exit(1)
    
    # 빌드 실행
    if build_exe():
        print("\n🧹 빌드 파일 정리하시겠습니까? (y/n): ", end="")
        response = input().lower()
        if response == 'y':
            clean_build()
            print("✅ 정리 완료!")
    
    print("\n🎯 사용법:")
    print("1. dist/BlogPhotoDownloader.app 파일을 Applications 폴더로 복사")
    print("2. Chrome 브라우저가 설치되어 있어야 합니다")
    print("3. 앱 파일을 더블클릭하여 웹페이지 이미지를 다운로드하세요!")
    print("4. 첫 실행 시 보안 경고가 나오면 시스템 환경설정에서 허용해주세요") 