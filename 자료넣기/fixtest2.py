import requests
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

def fetch_smp_data():
    """전기요금 데이터를 스크래핑하여 리스트로 반환"""
    smp = []
    now_hour = datetime.now().hour
    now_hour = 24 if now_hour == 0 else now_hour  

    url = "https://new.kpx.or.kr/smpInland.es?mid=a10606080100&device=pc#main"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        for i in range(now_hour - 7, now_hour + 1):
            cell = soup.select_one(
                f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child({i}) > td:nth-child(8)"
            )
            if cell:
                smp.append(float(cell.text.strip()))

        before_max, before_min = [], []
        for i in range(2, 9):
            max_cell = soup.select_one(
                f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(25) > td:nth-child({i})"
            )
            min_cell = soup.select_one(
                f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(26) > td:nth-child({i})"
            )

            if max_cell and min_cell:
                before_max.append(float(max_cell.text.strip()))
                before_min.append(float(min_cell.text.strip()))

        avg_max = round(sum(before_max) / len(before_max), 2) if before_max else 0
        avg_min = round(sum(before_min) / len(before_min), 2) if before_min else 0

        return smp, avg_max, avg_min, now_hour

    except Exception as e:
        print(f"데이터를 불러오는 중 오류 발생: {e}")
        return [], 0, 0, now_hour


def create_window():
    """Tkinter GUI 생성"""
    smp, avg_max, avg_min, now_hour = fetch_smp_data()
    
    def add_red_line():
        """경고선 추가 함수"""
        global red_line  
        try:
            set_money_value = float(setmoney_ent.get())  
            
            if red_line:
                red_line.remove()
                
            red_line = ax.axhline(y=set_money_value, color='red', linestyle='--')
            canvas.draw()
        except ValueError:
            print("유효한 숫자를 입력하세요.")  

    root = tk.Tk() 
    root.title("SmartElectricBill")
    root.geometry("620x880")

    price_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    price_frame.grid(row=0, pady=10, padx=10, sticky="w")

    tk.Label(price_frame, text="당월 누적 전기 요금").grid(row=0, column=0, padx=5, pady=5)
    maxmoney_ent = tk.Entry(price_frame, width=20, state="readonly") 
    maxmoney_ent.grid(row=0, column=1, padx=5)

    tk.Label(price_frame, text="최대 요금 설정").grid(row=1, column=0, padx=5, pady=5)
    limit_set_ent = tk.Entry(price_frame, width=20)
    limit_set_ent.grid(row=1, column=1, padx=5)
    tk.Button(price_frame, text="확인").grid(row=1, column=2, padx=5)

    week_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    week_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew", columnspan=1)

    tk.Label(week_frame, text="주간 최대 전기 요금").grid(row=0, column=0, padx=5, pady=5)
    week_max_ent = tk.Entry(week_frame, width=12, state="readonly")  
    week_max_ent.grid(row=0, column=1, padx=5)
    week_max_ent.insert(0, avg_max)

    tk.Label(week_frame, text="주간 최소 전기 요금").grid(row=1, column=0, padx=5, pady=5)
    week_min_ent = tk.Entry(week_frame, width=12, state="readonly")  
    week_min_ent.grid(row=1, column=1, padx=5)
    week_min_ent.insert(0, avg_min)

    warn_frame = tk.Frame(root, bd=2, relief="solid", padx=5, pady=5)
    warn_frame.grid(row=1, column=1, pady=10, padx=10, sticky="ew", columnspan=1)

    tk.Label(warn_frame, text="경고 요금 설정").grid(row=0, column=0, padx=5, pady=5)
    setmoney_ent = tk.Entry(warn_frame, width=12)  
    setmoney_ent.grid(row=0, column=1, padx=5)
    tk.Button(warn_frame, text="확인", command=add_red_line).grid(row=0, column=2, padx=5)

    fig = Figure(figsize=(6, 4), dpi=100)
    global ax, red_line
    ax = fig.add_subplot(111)
    ax.set_title("SMP (전기요금 변화)")
    
    hours_range = list(range(now_hour - 7, now_hour + 1))
    
    if len(smp) != len(hours_range):
        print("데이터 불일치: x =", len(hours_range), "y =", len(smp))
        smp = [0] * len(hours_range)  

    ax.plot(hours_range, smp, marker="o", linestyle="-", color="burlywood")
    
    for i, value in enumerate(smp):
        ax.text(hours_range[i], value + 0.2, f"{value:.2f}", fontsize=7, ha='center', va='bottom', color="black")
    
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("시간 (hour)")
    ax.set_ylabel("요금 (원/kWh)")

    red_line = None  

    canvas = FigureCanvasTkAgg(fig, master=root)  # ✅ aster → master 수정
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    root.mainloop()

create_window()