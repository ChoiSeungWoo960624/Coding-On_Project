import requests
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

def window():  
    def add_red_line():
        global red_line  
        try:
            set_money_value = float(setmoney_ent.get())  
            
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
 
    before_max = []
    before_min = []
    
    for i in range(2, 9):  
        before_max.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(25) > td:nth-child({i})").text.strip()))
        before_min.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(26) > td:nth-child({i})").text.strip()))

    avg_max = round(sum(before_max) / len(before_max), 2)  
    avg_min = round(sum(before_min) / len(before_min), 2)  

    root = tk.Tk() 
    root.title("SmartElectricBill")
    root.geometry("620x880")

    price_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    price_frame.grid(row=0, pady=10, padx=10, sticky="w")

    maxmoney_lab = tk.Label(price_frame, text="당월 누적 전기 요금")
    maxmoney_lab.grid(row=0, column=0, padx=5, pady=5)

    maxmoney_ent = tk.Entry(price_frame, width=20, background="white", state="readonly") 
    maxmoney_ent.grid(row=0, column=1, padx=5)

    limit_set_lab = tk.Label(price_frame, text="최대 요금 설정")  
    limit_set_lab.grid(row=1, column=0, padx=5, pady=5)

    limit_set_ent = tk.Entry(price_frame, width=20, background="white")  
    limit_set_ent.grid(row=1, column=1, padx=5)

    limit_set_btn = tk.Button(price_frame, text="확인")  
    limit_set_btn.grid(row=1, column=2, padx=5)

    # 📌 주간 요금 프레임 (주간 최대 & 최소 요금)
    week_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    week_frame.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    week_max_lab = tk.Label(week_frame, text="주간 최대 전기 요금")
    week_max_lab.grid(row=0, column=0, padx=5, pady=5)

    week_max_ent = tk.Entry(week_frame, width=20, background="white")
    week_max_ent.grid(row=0, column=1, padx=5)
    week_max_ent.insert(0, avg_max)
    week_max_ent.config(state="readonly")

    week_min_lab = tk.Label(week_frame, text="주간 최소 전기 요금")
    week_min_lab.grid(row=1, column=0, padx=5, pady=5)

    week_min_ent = tk.Entry(week_frame, width=20, background="white")
    week_min_ent.grid(row=1, column=1, padx=5)
    week_min_ent.insert(0, avg_min)
    week_min_ent.config(state="readonly")

    # 경고 요금 설정 프레임 (오른쪽 배치)
    warn_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    warn_frame.grid(row=1, column=1, pady=10, padx=10, sticky="w")

    setmony_lab = tk.Label(warn_frame, text="경고 요금 설정")
    setmony_lab.grid(row=0, column=0, padx=5, pady=5)

    setmoney_ent = tk.Entry(warn_frame, width=20, background="white")
    setmoney_ent.grid(row=0, column=1, padx=5)

    setmoney_btn = tk.Button(warn_frame, text="확인", command=add_red_line)  
    setmoney_btn.grid(row=0, column=2, padx=5)

    fig = Figure(figsize=(6, 4), dpi=100)
    global ax, red_line
    ax = fig.add_subplot(111)
    ax.set_title("SMP (전기요금 변화)")
    ax.plot(range(now_hour - 7, now_hour + 1), smp, marker="o", linestyle="-", color="burlywood")
    
    for i, value in enumerate(smp):
        ax.text(now_hour - 7 + i, value+0.2, f"{value:.2f}", fontsize=7, ha='center', va='bottom', color="black")
    
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("시간 (hour)")
    ax.set_ylabel("요금 (원/kWh)")

    red_line = None  

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    canvas.get_tk_widget().grid(row=4, pady=10, sticky="s")

    root.mainloop()

window()