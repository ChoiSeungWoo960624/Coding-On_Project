# 응용프로그램으로 쓰일 스크립트입니다.
# 함부로 수정하지 말고 Test.py 등으로 한번 테스트 한 뒤 merge 해주세요.

from tkinter import *
from bs4 import BeautifulSoup
import requests,time

def get_cost():
    #실시간 전기요금 가져오기.
    url="https://online.kepco.co.kr/"
    res=requests.get(url)
    soup=BeautifulSoup(res.text, "html.parser")
    time.sleep(2)
    prp=soup.select_one("#mf_wfm_layout_mainPwrReservePercent")
    print(prp)

get_cost()
