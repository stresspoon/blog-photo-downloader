import os
import time
import threading
import re
import requests
import urllib.parse
import subprocess
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

def get_unique_filename(save_path):
    """파일명 중복을 방지하기 위한 함수"""
    if not os.path.exists(save_path):
        return save_path
    
    base, ext = os.path.splitext(save_path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{ext}"):
        counter += 1
    return f"{base}_{counter}{ext}"

def download_images_from_page(page_url, download_dir, log_widget):
    import os, time, re, requests, urllib.parse
    from selenium.webdriver.common.by import By

    # 다운로드 폴더 생성
    os.makedirs(download_dir, exist_ok=True)

    # Selenium 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # ChromeDriver 자동 관리
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(page_url)
        time.sleep(2)

        # lazy-load 대응 스크롤
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(1)

        img_urls = set()

        # --- 이미지 URL 수집 함수 ---
        def collect(context_name):
            # img(src) + a(href)
            imgs = driver.find_elements(By.TAG_NAME, "img")
            links = driver.find_elements(By.TAG_NAME, "a")
            log_widget.insert(tk.END, f"🔍 [{context_name}] img 태그: {len(imgs)}, a 태그: {len(links)}\n")

            for img in imgs:
                src = img.get_attribute('src') or ""
                path = urllib.parse.urlparse(src).path.lower()
                ext = os.path.splitext(path)[1]
                if ext in ('.jpg','.jpeg','.png','.gif','.webp'):
                    full = urllib.parse.urljoin(page_url, src)
                    img_urls.add(full)
            for link in links:
                href = link.get_attribute('href') or ""
                path = urllib.parse.urlparse(href).path.lower()
                ext = os.path.splitext(path)[1]
                if ext in ('.jpg','.jpeg','.png','.gif','.webp'):
                    full = urllib.parse.urljoin(page_url, href)
                    img_urls.add(full)

            # inline background-image
            els = driver.find_elements(By.CSS_SELECTOR, "*[style*='background-image']")
            for el in els:
                style = el.get_attribute('style')
                m = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
                if m:
                    bg = urllib.parse.urljoin(page_url, m.group(1))
                    img_urls.add(bg)

        # 1) 메인 문서에서 수집
        collect("main")

        # 2) 모든 iframe 돌면서 수집
        frames = driver.find_elements(By.TAG_NAME, "iframe")
        log_widget.insert(tk.END, f"🔍 iframe 개수: {len(frames)}\n")
        for i, frame in enumerate(frames):
            src = frame.get_attribute('src')
            log_widget.insert(tk.END, f"  • iframe[{i}] src: {src}\n")
            try:
                driver.switch_to.frame(frame)
                collect(f"iframe[{i}]")
            except Exception as e:
                log_widget.insert(tk.END, f"❌ iframe[{i}] 스위치 오류: {e}\n")
            finally:
                driver.switch_to.default_content()

        # 3) 다운로드 실행
        if not img_urls:
            log_widget.insert(tk.END, "⚠️ 페이지에서 찾은 이미지가 없습니다.\n")
        else:
            log_widget.insert(tk.END, f"✅총 이미지 URL: {len(img_urls)}\n")
            for url in sorted(img_urls):
                fn = os.path.basename(urllib.parse.urlparse(url).path)
                save_path = os.path.join(download_dir, fn)
                save_path = get_unique_filename(save_path)  # 중복 방지
                try:
                    headers = {'Referer': page_url}
                    r = requests.get(url, headers=headers, stream=True, timeout=10)
                    if r.status_code == 200:
                        with open(save_path, 'wb') as f:
                            for chunk in r.iter_content(1024):
                                f.write(chunk)
                        log_widget.insert(tk.END, f"[OK] {os.path.basename(save_path)} 다운로드 완료\n")
                    else:
                        log_widget.insert(tk.END, f"[FAIL] {fn} ({r.status_code})\n")
                except Exception as e:
                    log_widget.insert(tk.END, f"[ERROR] {fn} 다운로드 중 오류: {e}\n")

    except Exception as e:
        log_widget.insert(tk.END, f"❌ 스크립트 오류: {e}\n")
    finally:
        driver.quit()
        log_widget.insert(tk.END, "✅ 작업 완료\n")

def create_gui():
    """GUI 인터페이스 생성"""
    root = tk.Tk()
    root.title("웹페이지 미디어 다운로더")
    root.geometry("900x700")  # 크기 증가
    root.minsize(800, 600)    # 최소 크기 설정
    
    # URL 입력 프레임
    url_frame = tk.Frame(root)
    url_frame.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Label(url_frame, text="웹페이지 URL:").pack(side=tk.LEFT)
    url_entry = tk.Entry(url_frame, width=60)
    url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    # 다운로드 폴더 선택 프레임
    folder_frame = tk.Frame(root)
    folder_frame.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Label(folder_frame, text="다운로드 폴더:").pack(side=tk.LEFT)
    folder_entry = tk.Entry(folder_frame, width=50)
    folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    folder_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads", "web_media"))
    
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder)
    
    tk.Button(folder_frame, text="폴더 선택", command=browse_folder).pack(side=tk.RIGHT)
    
    # 로그 출력 영역
    log_frame = tk.Frame(root)
    log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    tk.Label(log_frame, text="다운로드 로그:").pack(anchor=tk.W)
    log_widget = scrolledtext.ScrolledText(log_frame, height=20)
    log_widget.pack(fill=tk.BOTH, expand=True)
    
    # 버튼 프레임 (배경색 추가로 확인 가능하게)
    button_frame = tk.Frame(root, bg="#f0f0f0", relief="raised", bd=2)
    button_frame.pack(fill=tk.X, padx=10, pady=10)
    
    def start_download():
        url = url_entry.get().strip()
        folder = folder_entry.get().strip()
        
        if not url:
            messagebox.showerror("오류", "URL을 입력해주세요.")
            return
        
        if not folder:
            messagebox.showerror("오류", "다운로드 폴더를 선택해주세요.")
            return
        
        # URL 형식 검증
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 로그 초기화
        log_widget.delete(1.0, tk.END)
        log_widget.insert(tk.END, f"🚀 다운로드 시작...\n")
        log_widget.insert(tk.END, f"📁 URL: {url}\n")
        log_widget.insert(tk.END, f"📂 폴더: {folder}\n")
        log_widget.insert(tk.END, "-" * 50 + "\n")
        
        # 다운로드 버튼 비활성화
        download_btn.config(state=tk.DISABLED)
        
        # 별도 스레드에서 다운로드 실행
        def download_thread():
            try:
                download_images_from_page(url, folder, log_widget)
            except Exception as e:
                log_widget.insert(tk.END, f"❌ 예상치 못한 오류: {e}\n")
            finally:
                # 다운로드 완료 후 버튼 활성화
                download_btn.config(state=tk.NORMAL)
                log_widget.insert(tk.END, "🎉 모든 작업이 완료되었습니다!\n")
        
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()
    
    # 다운로드 시작 버튼 (크고 눈에 띄게)
    download_btn = tk.Button(button_frame, text="🚀 다운로드 시작", command=start_download, 
                           bg="#4CAF50", fg="white", font=("Arial", 14, "bold"), 
                           height=2, width=15)
    download_btn.pack(side=tk.LEFT, padx=10, pady=5)
    
    def clear_log():
        log_widget.delete(1.0, tk.END)
    
    # 로그 지우기 버튼
    clear_btn = tk.Button(button_frame, text="📝 로그 지우기", command=clear_log,
                         bg="#FF5722", fg="white", font=("Arial", 10, "bold"),
                         height=2, width=12)
    clear_btn.pack(side=tk.LEFT, padx=10, pady=5)
    
    def open_folder():
        folder = folder_entry.get().strip()
        if folder and os.path.exists(folder):
            try:
                if platform.system() == "Windows":
                    os.startfile(folder)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.call(["open", folder])
                else:  # Linux
                    subprocess.call(["xdg-open", folder])
            except Exception as e:
                messagebox.showerror("오류", f"폴더를 열 수 없습니다: {e}")
        else:
            messagebox.showwarning("경고", "폴더가 존재하지 않습니다.")
    
    # 폴더 열기 버튼
    folder_btn = tk.Button(button_frame, text="📁 폴더 열기", command=open_folder,
                          bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                          height=2, width=12)
    folder_btn.pack(side=tk.LEFT, padx=10, pady=5)
    
    return root

if __name__ == "__main__":
    try:
        root = create_gui()
        root.mainloop()
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        input("엔터를 눌러 종료하세요...")
