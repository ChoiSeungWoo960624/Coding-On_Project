
import requests
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


plt.rcParams["font.family"] = "Malgun Gothic"  
plt.rcParams["axes.unicode_minus"] = False  

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

    avg_max = round(sum(before_max) / len(before_max), 2)  # 7일간 평균 최대 요금
    avg_min = round(sum(before_min) / len(before_min), 2)  # 7일간 평균 최소 요금
    avg_today = float(soup.select_one("#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(27) > td:nth-child(8)").text)  # 오늘의 평균 요금

    print(f"현 시각: {now_hour}시  |  실시간 전기요금: {smp}원/kWh")
    print(f"7일간 평균 최대 요금: {avg_max}")
    print(f"7일간 평균 최소 요금: {avg_min}")
    print(f"오늘 평균 요금: {avg_today}")

def window():  # Tkinter로 창을 띄우는 함수
    def add_red_line():
        global red_line  # 전역 변수 선언
        try:
            # setmoney_ent에 입력된 값 받기
            set_money_value = float(setmoney_ent.get())  # 사용자 입력값
            
            # 기존 경고선이 있다면 삭제
            if red_line is not None:
                red_line.remove()
            
            
            red_line = ax.axhline(y=set_money_value, color='red', linestyle='--')
            
           
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

    root = tk.Tk()  # 루트창 생성
    root.title("SmartElectricBill")
    root.geometry("620x880")
    
    """
    # 왼쪽으로 프레임 생성
    leftframe = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5) # 라벨과 입력 필드를 감싸는 프레임 생성 
    # (bd=2, relief="solid", padx=5, pady=5) 없애면 테두리 없어져요
    leftframe.grid(row=0, pady=10, padx=10, sticky="w")
    """

    # 첫 번째 프레임 (최대 요금 설정 및 경고 요금 설정)
    price_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    price_frame.grid(row=0, pady=10, padx=10, sticky="w")

    # 최대 요금 설정
    max_frame = tk.Frame(price_frame)
    max_frame.grid(row=0, column=0, padx=5, pady=5)
    maxmoney_lab = tk.Label(max_frame, text="최대 요금 설정")
    maxmoney_lab.pack()
    maxmoney_ent = tk.Entry(price_frame, width=20, background="white")
    maxmoney_ent.grid(row=0, column=1, pady=1, padx=5, sticky="w")
    maxmoney_btn = tk.Button(price_frame, text="확인")
    maxmoney_btn.grid(row=0, column=2, padx=5)

    # 경고 요금 설정
    frame = tk.Frame(price_frame)
    frame.grid(row=1, column=0, padx=5, pady=5)
    setmony_lab = tk.Label(frame, text="경고 요금 설정")
    setmony_lab.pack()
    setmoney_ent = tk.Entry(price_frame, width=20, background="white")
    setmoney_ent.grid(row=1, column=1, pady=1, padx=5, sticky="w")
    setmoney_btn = tk.Button(price_frame, text="확인")
    setmoney_btn.grid(row=1, column=2, padx=5)

    # 두 번째 프레임 (주간 최대 및 최소 전기 요금)
    week_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    week_frame.grid(row=1, pady=10, padx=10, sticky="w")

    # 주간 최대 전기 요금
    week_max_frame = tk.Frame(week_frame)
    week_max_frame.grid(row=0, column=0, padx=5, pady=5)
    week_max_lab = tk.Label(week_max_frame, text="주간 최대 전기 요금")
    week_max_lab.pack()
    week_max_ent = tk.Entry(week_frame, width=20, background="white")
    week_max_ent.grid(row=0, column=1, pady=1, padx=5, sticky="w")

    # 주간 최소 전기 요금
    week_min_frame = tk.Frame(week_frame)
    week_min_frame.grid(row=1, column=0, padx=5, pady=5)
    week_min_lab = tk.Label(week_min_frame, text="주간 최소 전기 요금")
    week_min_lab.pack()
    week_min_ent = tk.Entry(week_frame, width=20, background="white")
    week_min_ent.grid(row=1, column=1, pady=1, padx=5, sticky="w")

    # 그래프 생성
    fig = Figure(figsize=(6, 4), dpi=100)
    global ax, red_line
    ax = fig.add_subplot(111)
    ax.set_title("SMP (전기요금 변화)")
    ax.plot(range(now_hour - 7, now_hour + 1), smp, marker="o", linestyle="-", color="burlywood")
    
    # 마커 위에 값 표시
    for i, value in enumerate(smp):
        ax.text(now_hour - 7 + i, value+0.19, f"{value:.3f}", fontsize=7, ha='center', va='bottom', color="black")
    
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("시간 (hour)")
    ax.set_ylabel("요금 (원/kWh)")
    
    red_line = None  # 초기 경고선 변수를 None으로 설정

    # 그래프를 Tkinter 창에 삽입
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # 그래프를 맨 밑에 배치
    canvas.get_tk_widget().grid(row=1, pady=10, sticky="s")

    root.mainloop()

window()