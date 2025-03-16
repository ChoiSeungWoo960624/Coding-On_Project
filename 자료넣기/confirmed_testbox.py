import requests
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

# 한글 폰트 설정 - Windows에서 실행할 경우 적용 필요 <- 안하면 깨져요요
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows 환경용 한글 폰트
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지

def get_cost():  # 실시간 전기요금을 가져오는 함수
    before_max = []
    before_min = []
    now_hour = int(datetime.now().strftime("%H"))
    
    if now_hour == 0:
        now_hour = 24

    url = "https://new.kpx.or.kr/smpInland.es?mid=a10606080100&device=pc#main"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    smp = float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child({now_hour}) > td:nth-child(8)").text)

    for i in range(2, 9):
        before_max.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(25) > td:nth-child({i})").text.strip()))
        before_min.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(26) > td:nth-child({i})").text.strip()))

    avg_max = round(sum(before_max) / len(before_max), 2)  
    avg_min = round(sum(before_min) / len(before_min), 2)  
    avg_today = float(soup.select_one("#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(27) > td:nth-child(8)").text)  

    print(f"현 시각: {now_hour}시  |  실시간 전기요금: {smp}원/kWh")
    print(f"7일간 평균 최대 요금: {avg_max}")
    print(f"7일간 평균 최소 요금: {avg_min}")
    print(f"오늘 평균 요금: {avg_today}")

def window():  # Tkinter로 창을 띄우는 함수
    def add_red_line():
        global red_line  # 전역 변수 선언
        try:
            # setmoney_ent에 입력된 값 받기
            set_money_value = float(setmoney_ent.get())  
            
            # 기존 경고선이 있다면 삭제
            if red_line is not None:
                red_line.remove()

            # 새롭게 빨간 선 추가
            red_line = ax.axhline(y=set_money_value, color='red', linestyle='--')
            
            # 그래프 다시 그리기
            canvas.draw()

        except ValueError:
            print("유효한 숫자를 입력하세요.")  

    smp = []
    now_hour = int(datetime.now().strftime("%H"))
    
    if now_hour == 0:
        now_hour = 24

    url = "https://new.kpx.or.kr/smpInland.es?mid=a10606080100&device=pc#main"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    for i in range(now_hour - 7, now_hour + 1):
        smp.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text.strip()))
 
 # 주간 최대 및 최소 전기 요금 가져오기
    before_max = []
    before_min = []
    
    for i in range(2, 9):  
        before_max.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(25) > td:nth-child({i})").text.strip()))
        before_min.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(26) > td:nth-child({i})").text.strip()))

    avg_max = round(sum(before_max) / len(before_max), 2)  
    avg_min = round(sum(before_min) / len(before_min), 2)  

    root = tk.Tk() # 루트창 생성
    root.title("SmartElectricBill")
    root.geometry("620x880")

    # 첫 번째 프레임 (당월 누적 전기 요금 설정 및 최대 요금 설정)
    price_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5) # 라벨과 입력 필드를 감싸는 프레임 생성
    # (bd=2, relief="solid", padx=5, pady=5) 없애면 테두리 없어져요
    price_frame.grid(row=0, pady=10, padx=10, sticky="w")

    # 당월 누적 전기 요금 설정
    maxmoney_lab = tk.Label(price_frame, text="당월 누적 전기 요금")
    maxmoney_lab.grid(row=0, column=0, padx=5, pady=5)

    maxmoney_ent = tk.Entry(price_frame, width=20, background="white", state="readonly") # state 부분 삭제하면 읽기 전용사라져요요
    maxmoney_ent.grid(row=0, column=1, padx=5)

    # 최대 요금 설정
    limit_set_lab = tk.Label(price_frame, text="최대 요금 설정")  
    limit_set_lab.grid(row=1, column=0, padx=5, pady=5)

    limit_set_ent = tk.Entry(price_frame, width=20, background="white")  
    limit_set_ent.grid(row=1, column=1, padx=5)

    limit_set_btn = tk.Button(price_frame, text="확인")  
    limit_set_btn.grid(row=1, column=2, padx=5)

    # 두 번째 프레임 (주간 최대 및 최소 전기 요금)
    week_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    week_frame.grid(row=1, pady=10, padx=10, sticky="w")

    # 주간 최대 전기 요금
    week_max_lab = tk.Label(week_frame, text="주간 최대 전기 요금")
    week_max_lab.grid(row=0, column=0, padx=5, pady=5)
    week_max_ent = tk.Entry(week_frame, width=20, background="white")
    week_max_ent.grid(row=0, column=1, padx=5)
    week_max_ent.insert(0, avg_max)
    week_max_ent.config(state="readonly")  # 읽기 전용

    # 주간 최소 전기 요금
    week_min_lab = tk.Label(week_frame, text="주간 최소 전기 요금")
    week_min_lab.grid(row=1, column=0, padx=5, pady=5)
    week_min_ent = tk.Entry(week_frame, width=20, background="white")
    week_min_ent.grid(row=1, column=1, padx=5)
    week_min_ent.insert(0, avg_min)
    week_min_ent.config(state="readonly")  # 읽기 전용  

    # 경고 요금 설정 (사용자가 입력 가능)
    limit_set_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)  
    limit_set_frame.grid(row=3, pady=10, padx=10, sticky="w")  # row=3 위치치

    setmony_lab = tk.Label(limit_set_frame, text="경고 요금 설정")
    setmony_lab.grid(row=0, column=0, padx=5, pady=5)

    setmoney_ent = tk.Entry(limit_set_frame, width=20, background="white")
    setmoney_ent.grid(row=0, column=1, padx=5)

    setmoney_btn = tk.Button(limit_set_frame, text="확인", command=add_red_line)  
    setmoney_btn.grid(row=0, column=2, padx=5)

    # 그래프 생성
    fig = Figure(figsize=(6, 4), dpi=100)
    global ax, red_line
    ax = fig.add_subplot(111)
    ax.set_title("SMP (전기요금 변화)")
    ax.plot(range(now_hour - 7, now_hour + 1), smp, marker="o", linestyle="-", color="burlywood")
    
     # 마커 위에 값 표시
    for i, value in enumerate(smp):
        ax.text(now_hour - 7 + i, value+0.2, f"{value:.2f}", fontsize=7, ha='center', va='bottom', color="black")
    
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("시간 (hour)")
    ax.set_ylabel("요금 (원/kWh)")

    red_line = None  # 초기 경고선 변수를 None으로 설정

    # 그래프를 Tkinter 창에 삽입
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # 그래프를 맨 밑에 배치
    canvas.get_tk_widget().grid(row=4, pady=10, sticky="s")

    root.mainloop()

window()