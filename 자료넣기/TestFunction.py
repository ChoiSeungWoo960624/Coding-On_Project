import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager, rc
import seaborn as sns
import numpy as np
### HeatMap 만드는 곳입니다.
# 한글폰트 적용
path = 'C:\\Windows\\Fonts\\malgun.ttf'  # 맑은 고딕 폰트 경로
font = font_manager.FontProperties(fname=path).get_name()
rc('font', family=font)

# 1. CSV 파일 읽기
ref= pd.read_csv("csv/15~23년 전력통계.csv")
df1 = pd.read_csv("comp_data_2020.csv", index_col=0)  # 첫 번째 열을 index로 설정
df2 = pd.read_csv("comp_data_2021.csv", index_col=0)  # 첫 번째 열을 index로 설정
df3 = pd.read_csv("comp_data_2022.csv", index_col=0)  # 첫 번째 열을 index로 설정
df4 = pd.read_csv("comp_data_2023.csv", index_col=0)  # 첫 번째 열을 index로 설정
# 3. 서브플롯 설정 (2x3 배열로 5개의 그래프, 하나는 비어 있음)
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
# 2. 히트맵 그리기
sns.heatmap(df1, cmap="crest", annot=False, cbar=True, ax=axes[0, 0])
sns.heatmap(df2, cmap="crest", annot=False, cbar=True, ax=axes[0, 1])
sns.heatmap(df3, cmap="crest", annot=False, cbar=True, ax=axes[1, 0])
sns.heatmap(df4, cmap="crest", annot=False, cbar=True, ax=axes[1, 1])

axes[0, 0].set_title("2020 절약한 전력비")
axes[0, 1].set_title("2021 절약한 전략비")
axes[1, 0].set_title("2022 절약한 전력비")
axes[1, 1].set_title("2023 절약한 전력비")


plt.tight_layout()
# 3. 그래프 설정


# 4. 출력
plt.show()
