import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager, rc
import seaborn as sns
import numpy as np

################# [ 여기 박스 안의 a,b만 수정하며 테스트해보세요~ ] ######################
a = 0.5  # 경고비 (최소금액~최대금액:0~100%로 봤을때 몇%를 경고금액으로 둘것인가?)
b = 0.7  # 낭비비 (경고금액을 넘었을 때 얼마나 절약하지 않을것인가?)
#############################################################################################

# 한글폰트 적용
path = 'C:\\Windows\\Fonts\\malgun.ttf'  # 맑은 고딕 폰트 경로
font = font_manager.FontProperties(fname=path).get_name()
rc('font', family=font)

# CSV 파일 불러오기
smp = "csv/smp_land_2023.csv"
df_smp = pd.read_csv(smp, parse_dates=['구분'])  # '구분' 컬럼을 datetime으로 변환

real = "csv/15~23년 전력통계.csv"
real = pd.read_csv(real)

def PastYearAvg():
    """ 기존 3단 누진세 방법 시행 시 가구당 평균 연간 전기요금 """
    for col in ['가구당 1년 전기요금(원)', '가구당 1년전력소비량(kWh)']:
        real[col] = real[col].astype(str).str.replace(",", "").astype(int)
    return real[['연도(년)', '가구당 1년 전기요금(원)', '가구당 1년전력소비량(kWh)']]

def AvrHourElec(year):
    """ 해당 연도 가구당 1시간 평균 소비전력 (kWh/h) 계산 """
    row = real.loc[real['연도(년)'] == year]
    if row.empty:
        return 0  # 데이터가 없으면 0 반환

    watt = int(str(row['가정용판매전력량(MWh)'].values[0]).replace(",", ""))
    popu = int(str(row['가정용수용호수(호)'].values[0]).replace(",", ""))
    return (watt * 1000) / popu / 365 / 24

def RealToSMP(warn_rate=0.5, weast_rate=0.5):
    """ SEB 시행 시 전기요금 및 사용량 계산 """
    year_cost = {year: {"cost": 0, "power": 0} for year in range(2020, 2024)}

    for date in df_smp['구분']:
        year = date.year
        if year not in year_cost:
            continue

        elec_hour_avr_year = AvrHourElec(year)
        start_date = date - pd.Timedelta(days=6)  # 최근 7일(오늘 포함)
        recent_data = df_smp[df_smp['구분'].between(start_date, date)]  # 안전한 필터링 방법

        if recent_data.empty:
            continue

        max_cost = recent_data["최대"].max()
        min_cost = recent_data["최소"].min()
        warn_cost = (warn_rate * (max_cost - min_cost)) + min_cost

        for hour in range(1, 25):
            hour_column = f"{hour}h"
            smp_price_series = df_smp.loc[df_smp['구분'] == date, hour_column]

            if smp_price_series.empty:
                continue

            smp_price = smp_price_series.values[0]

            if smp_price > warn_cost:
                year_cost[year]["cost"] += smp_price * elec_hour_avr_year * weast_rate
                year_cost[year]["power"] += elec_hour_avr_year * weast_rate
            else:
                year_cost[year]["cost"] += smp_price * elec_hour_avr_year
                year_cost[year]["power"] += elec_hour_avr_year

    # 딕셔너리 → 데이터프레임 변환
    result_df = pd.DataFrame.from_dict(year_cost, orient='index').reset_index()
    result_df.columns = ["연도(년)", "전기요금(원)", "소모전력(kWh)"]

    return result_df.astype({"전기요금(원)": int, "소모전력(kWh)": int})

def heat_df(): #해당연도 얼마나 전력을 아꼈는가?
    """ 경고비(warn_rate)와 낭비비(weast_rate)에 따른 전력 소비량 변화 """
    waste_rates = np.round(np.arange(0.0, 1.1, 0.1), 2)
    warn_rates = np.round(np.arange(0.0, 1.1, 0.1), 2)
    heat_dict = {waste: {} for waste in waste_rates}  # 변경된 딕셔너리 구조

    for warn in warn_rates:
        print(f"경고비 {warn} 분석 중...")
        for waste in waste_rates:
            print(f"경고비 {warn}, 낭비비 {waste} 분석 중...")
            result = RealToSMP(warn, waste)
            heat_dict[waste][warn] = result['소모전력(kWh)'].sum()

    df_heat = pd.DataFrame.from_dict(heat_dict, orient='index')
    df_heat.index.name = "낭비비"
    df_heat.columns.name = "경고비"
    df_heat.to_csv("heatmap_data_2023.csv", encoding="utf-8-sig")

    return df_heat


# df_result = heat_df()
# print(df_result.head())

def comp():
    waste_rates = np.round(np.arange(0.0, 1.1, 0.1), 1)  # np.float64 대신 float로
    warn_rates = np.round(np.arange(0.0, 1.1, 0.1), 1)  # np.float64 대신 float로
    comp_dict = {waste: {} for waste in waste_rates}
    
    # 각 연도별 데이터프레임을 읽어옵니다.
    # df1 = pd.read_csv("heatmap_data_2020.csv", index_col=0)
    # df2 = pd.read_csv("heatmap_data_2021.csv", index_col=0)
    # df3 = pd.read_csv("heatmap_data_2022.csv", index_col=0)
    df4 = pd.read_csv("heatmap_data_2023.csv", index_col=0)
    df4.columns = pd.to_numeric(df4.columns, errors='coerce')  # 변환할 수 없는 값은 NaN으로 처리
    print("df1 컬럼 타입:", df4.columns)

    # df1의 인덱스도 float로 변환 (필요한 경우)
    df4.index = df4.index.astype(float)
    for waste in waste_rates:
        print("낭비비",waste)
        for warn in warn_rates:
            print("낭비비",waste,"경고비",waste,"분석중")
            comp_dict[waste][warn]=round(df4.loc[warn,waste]/5763,2)
        else :
            print("버그 발생")
    df_comp = pd.DataFrame.from_dict(comp_dict, orient='index')
    df_comp.index.name = "낭비비"
    df_comp.columns.name = "경고비"
    df_comp.to_csv("comp_data_2023.csv", encoding="utf-8-sig")

    return df_comp

comp()