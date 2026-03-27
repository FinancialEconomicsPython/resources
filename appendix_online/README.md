# 온라인 부록

---
## 한센-자가나단 바운드(Hansen-Jagannathan bound)

- FE_appendix_HJbound.pdf
- FE_appendix_HJounbd.ipynb (데이터를 이용해 HJ 바운드를 그리는 파이썬 노트북)

비모수적 방법으로 확률적 할인인자(SDF: Stochastic Discount Factor)의 1차 적률 $E(m)$, 2차 적률 $\sigma(m)$이 
금융시장의 데이터를 설명하기 위해 어떤 조건을 가져야 하는지 설명하는 이론입니다. 이를 통해 (우리 책의 맥락에서는) 주식 프리미엄 퍼즐을 
설명하기 위해서 어떤 조합의 $(E(m), \sigma(m))$가 필요한지 알 수 있고, 어떤 모형이 적절한지 비교 및 판단할 수 있습니다. 

<img src="https://raw.githubusercontent.com/FinancialEconomicsPython/resources/main/figures/HJbound.png" width="700">


--- 
## 엡스타인-진(Epstein-Zin) 효용함수

- FE_appendix_EZpreference.pdf

6장에서 CRRA 효용함수를 이용해 주식 수익률 퍼즐을 살펴 보았는데 $\gamma$ 모수가 상대적 위험기피계수 $\gamma$, 그리고 동시에
시점간 대체탄력도(EIS: Elasticiaty of Intertemporal Substitution) $1/\gamma$의 역할 두 가지를 동시에 하고 있습니다. 
엡스타인-진 효용함수는 이 두 가지 구분되는 성격의 모수를 분리해서 각각 가지고 있습니다. 엡스타인-진 효용함수란 무엇인가, 이 경우 SDF는 어떤
형태를 가지고 있나, 이를 통해 어떻게 주식 프리미엄 퍼즐을 설명할 수 있나 살펴봅니다. 

--- 
## 우리나라 인플레이션 분석

- inflation_joyplot.ipynb (joyplot을 그리는 파이썬 노트북)
- inflation_various.ipynb (기조적 물가지표를 그리는 파이썬 노트북, coming soon)

우리나라 데이터를 이용해서 joy plot, 기조적 물가지표 등을 그리는 파이썬 코드입니다. 기조적 물가지표에는 관리 제외 근원물가,
조정평균물가, 가중중위수물가, 관리 제외 경직적 물가, 경기민감 근원 물가 등이 있습니다. 

