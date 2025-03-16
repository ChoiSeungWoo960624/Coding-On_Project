# SmartElectricBill Project⚡

- [x] 실시간전기요금확인 요금청구 어플리케이션

## 📝 프로젝트 소개

* **주제**  
  실시간 전기 요금 제어 및 절감 효과 분석 시스템

* **기획 의도**  
  전력 사용량 및 전기 요금 절감, 그리고 전력 예비율 조절을 위한 실시간 전기 요금제의 실용성을 증명하기 위해 본 프로젝트를 진행하였습니다. 또한, 정부가 도입을 고려했던 도매 가격 기반의 전기 요금 설정과 그로 인한 절감 효과를 시각적으로 보여주는 어플리케이션을 개발하고, 이로써 관련 분야에 도움이 되고자 했습니다.

* **기간**  
  2025.02.05 ~ 2025.02.17 (12일)

## 🛠️사용한 기술

|카테고리|기술|
|:-|:-:|
|언어|파이썬|
|데이터수집|리퀘스트(request), 뷰티풀수프(Beatuifulsoup)|
|전처리과정|판다스(Pandas),넘파이(Numpy)|
|도표시각화|맷플롯립(matplotlib),씨본(Seaborn)|
|UI시각화|티킨터(Tkinter), FigureCanvasTkAgg(피규어캔버스)|

## 💡주요기술 채택이유
* 본 프로젝트에서는 그간 배운 기술들을 실전에서 적용해 보고자 하였으며, 데이터 수집부터 시각화, UI 구현까지 전반적인 과정을 경험할 수 있도록 주요 기술을 선정하였습니다.

| 카테고리     | 기술                                          | 채택 이유                                                                                             |
|--------------|-----------------------------------------------|------------------------------------------------------------------------------------------------------|
| **언어**     | 파이썬 (Python)                               | 데이터 수집부터 시각화, UI 구현까지 전 과정에서 활용 가능하며, 다양한 라이브러리를 지원하여 개발 효율성을 높일 수 있기 때문 |
| **데이터 수집** | 리퀘스트 (Requests), 뷰티풀수프 (BeautifulSoup) | 웹에서 필요한 데이터를 자동으로 가져와 분석할 수 있도록 하기 위해 사용                            |
| **전처리 과정** | 판다스 (Pandas), 넘파이 (NumPy)               | 수집된 데이터를 효율적으로 정리·가공하고, 연산 및 분석을 용이하게 하기 위해 활용                   |
| **도표 시각화** | 맷플롯립 (Matplotlib), 씨본 (Seaborn)         | 전기 요금 절감 효과를 시각적으로 표현하고, 데이터의 패턴을 보다 직관적으로 파악할 수 있도록 하기 위해 선택 |
| **UI 시각화**  | 티킨터 (Tkinter), FigureCanvasTkAgg (피규어캔버스) | 전기 요금 절감 효과를 시각적으로 표현하고, 데이터의 패턴을 보다 직관적으로 파악할 수 있도록 하기 위해 선택 |


## 🙋‍♂️내가 구현한 기능




## 🌲프로젝트 구조

```python
*
|-- 자료         # 프로젝트를 진행하는데 참고 및 도움이 된 자료들 보관
|-- 자료넣기      # 프로젝트 기능 구현을 위한 시행착오 코드 및 테스트용 코드 모음
|-- comp파일     # 연도별 낭비비와 경고비 비용 대비 효율성을 보여주는 데이터 csv파일 모음음
|-- csv          # csv 데이터 파일들 보관
|-- heatmap  # heatmapmaker.py -heatmap 그래프를 만드는 기능과 히트맵필요한 csv파일일
|- ppt_plot.py      # 경고비와 낭비비를 임의로 설정하며 그래프로 나타내는 기능
|- Prototype.py     # 실전에서 어떻게 사용될지 예시를 보여주기 위해 Tkinter를 이용해 인터페이스를 구현함
|- SmartElectric.py # 프로젝트에 필요한 각종 함수를 모아둔 모듈용 파일
```
