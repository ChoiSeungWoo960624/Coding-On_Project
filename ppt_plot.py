# 이 곳은 PPT에 올라갈 자료들을 시각화 하는 파일입니다.
# 함부로 수정하지마세요~

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager


# 한글폰트 적용
path = 'C:\\Windows\\Fonts\\malgun.ttf'  # 맑은 고딕 폰트 경로
font = font_manager.FontProperties(fname=path).get_name()

file_name="csv/smp_land_2023.csv"
df=pd.read_csv(file_name)
df = df.rename(columns=lambda x: x.strip())  # 공백 제거

print(df.head()) # 구분(일자), 1h~24h(시간), 값(요금)
# print(df.info()) # 결측값이 없다. 예@@@@!


print(df['평균'].values.mean())

df['월별']=df['구분'].astype(str).str[:6]

month_avg_bill=df.groupby('월별')['평균'].mean()
print(month_avg_bill)




##################################################################################################################
def gragh(x,y,title): #그래프를 생성하는 함수
    plt.rc('font', family=font)
    # 그래프 그리기
    plt.plot(x, y, marker='o')
    plt.xlabel('시간 (시간 단위)')
    plt.ylabel('가격 (원)')
    # 그래프 제목
    plt.title(title)
    # 마커 위에 숫자 표시
    for i, txt in enumerate(y):
        plt.text(x[i],y[i]+1, f'{txt:.2f}',ha='center',fontsize=10, color='black')
    plt.xticks(x)
    plt.yticks(range(int((min(y)//10)*10-5), int(max(y))+15,int((min(y)//10))))
    plt.grid(True, linestyle='--', alpha=0.5)  # 격자 추가
    # 그래프 표시
    plt.show()

# 그래프 데이터
x = [1, 2, 3, 4, 5,6,7,8,9,10,11,12]
y = month_avg_bill
title="2024년 월별 전기요금"
gragh(x,y,title)#함수 실행
