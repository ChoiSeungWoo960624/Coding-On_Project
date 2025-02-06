# 모듈로 쓰일 스크립트입니다.
# 함수 기능만 만들어주세요. 실제 프로그램은 다른 py에서 구현할 예정입니다.

import requests
import pandas as pd
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bs4 import BeautifulSoup
from datetime import datetime



def get_cost():  #실시간 전기요금을 가져오는 함수
    before_max=[]
    before_min=[]
    now_hour=datetime.now().strftime("%H")
    if now_hour == 0:
        now_hour=24
    url="https://new.kpx.or.kr/smpInland.es?mid=a10606080100&device=pc#main"
    res=requests.get(url)
    soup=BeautifulSoup(res.text, "html.parser")
    smp=float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child({now_hour}) > td:nth-child(8)").text)
    for i in range(2,9):
        before_max.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(25) > td:nth-child({i})").text.strip()))
        before_min.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(26) > td:nth-child({i})").text.strip()))
    avg_max=round(sum(before_max)/len(before_max),2) #7일간 평균최대요금
    avg_min=round(sum(before_min)/len(before_min),2) #7일간 평균최소요금
    avg_today=float(soup.select_one("#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child(27) > td:nth-child(8)").text) #오늘의 평균요금이다.
    print(f"현 시각:{now_hour}시  |  실시간 전기요금 :{smp}원/kWh")
    print(f"7일간 평균 최대요금 : {avg_max}")
    print(f"7일간 평균 최소요금 : {avg_min}")
    print(f"오늘 평균 요금 : {avg_today}")

def save_bill(): # 최대 목표 요금 을 설정하는 함수 (한달동안 최대 얼마의 요금을 생각하는지...)
    pass


def window(): # tkinter로 창을 띄우는 함수
    def add_red_line():
        try:
            # setmoney_ent에 입력된 값 받기
            set_money_value = float(setmoney_ent.get())  # 사용자 입력값
            ax.axhline(y=set_money_value, color='red', linestyle='--')  # 빨간 선 추가
            canvas.draw()  # 그래프 다시 그리기
        except ValueError:
            print("유효한 숫자를 입력하세요.")
    smp=[]
    now_hour=int(datetime.now().strftime("%H"))
    if now_hour == 0:
        now_hour=24
    url="https://new.kpx.or.kr/smpInland.es?mid=a10606080100&device=pc#main"
    res=requests.get(url)
    soup=BeautifulSoup(res.text, "html.parser")
    for i in range(now_hour-7,now_hour+1):
        smp.append(float(soup.select_one(f"#contents_body > div.content_style > div.conTableGroup.scroll > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text.strip()))
    root=tk.Tk() #루트창 생성
    root.title("SmartElectricBill")
    topframe=tk.Frame(root)
    topframe.pack()
    setmony_lab=tk.Label(topframe, text="경고요금 설정")
    setmoney_ent=tk.Entry(topframe,width=20,background="lightcyan")
    setmoney_btn=tk.Button(topframe, text="확인",command=add_red_line)
    setmony_lab.grid(row=0,column=0,pady=1,sticky='w')
    setmoney_ent.grid(row=1,column=0,pady=1,padx=1,sticky="w")
    setmoney_btn.grid(row=1,column=1,padx=1)
    fig = Figure(figsize=(6,4) ,dpi=100) #그래프 생성
    ax=fig.add_subplot(111)
    ax.set_title("SMP")
    ax.plot(range(now_hour-7,now_hour+1),smp,marker="o")
    ax.set_xlabel("time(hour)")
    ax.set_ylabel("cost(won/Kwh)")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    root.mainloop()

window()