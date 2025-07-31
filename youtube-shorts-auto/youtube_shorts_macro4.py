import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import math

driver = None  # 글로벌로 선언

def play_shorts_loop(video_url):
    global driver
    try:
        opts = Options()
        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-infobars")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        driver.get("https://accounts.google.com/signin")

        messagebox.showinfo("로그인", "로그인 완료 후 확인 버튼을 누르세요")

        while True:
            try:
                driver.get(video_url)
                time.sleep(3)

                # 영상 재생
                driver.execute_script("""
                    const video = document.querySelector('video');
                    if (video) {
                        video.muted = false;
                        video.play();
                    }
                """)

                # duration 추출
                duration = 0
                for _ in range(10):
                    try:
                        duration = driver.execute_script("return document.querySelector('video')?.duration")
                        if duration and not math.isnan(duration):
                            break
                    except:
                        pass
                    time.sleep(1)

                if not duration or math.isnan(duration):
                    duration = 15  # fallback

                # 영상 재생 시간 체크
                while True:
                    current_time = driver.execute_script("return document.querySelector('video')?.currentTime || 0")
                    if current_time >= duration - 0.5:
                        break
                    time.sleep(0.5)

            except Exception as e:
                print("오류 발생:", e)

            time.sleep(1)

    except Exception as e:
        messagebox.showerror("오류", f"실행 중 오류 발생: {e}")

def start_macro():
    url = url_entry.get().strip()
    if not url.startswith("http"):
        messagebox.showwarning("URL 오류", "정확한 Shorts 영상 URL을 입력하세요.")
        return
    threading.Thread(target=play_shorts_loop, args=(url,), daemon=True).start()

# --- GUI ---
root = tk.Tk()
root.title("YouTube Shorts 반복재생기")
root.geometry("400x200")

tk.Label(root, text="반복 재생할 Shorts 영상 URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

start_btn = tk.Button(root, text="재생 시작", command=start_macro)
start_btn.pack(pady=20)

root.mainloop()
