import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px


st.title('Climate Change and Asset Pricing')

st.write("""
In recent years, the financial industry has increasingly recognized the importance of climate risk. 
Climate information providers (CIPs) have been producing scenario-based analyses to quantify the financial risks associated with climate change.
         """)

st.write("""The typical approach involves the use of **discounted cashflows (DCF)** to value assets, **conditional on a climate scenario**, interpreted as a plausible future state of the world. In a
         simple one-period model, the approach can be summarized as follows:
            """)

st.latex(r"""
         P(s) = \frac{ CF(s)_{t+1}}{1 + r_{t+1}}
         """)

st.write("""
         with $P(s)$ the price of the asset in scenario $s$, $CF(s)_{t+1}$ the cash flow received at time $t+1$ in scenario $s$, and $r_{t+1}$ the discount rate applicable at that time.
         **You may notice that the discount rate is not conditioned on the scenario**.""")

st.write("""
        The cashflows $CF(s)_{t+1}$ are typically modelled as a sensitivity of the asset's cash flows to the climate scenario $s$:
         """)

st.latex(r"""
         CF(s)_{t+1} = \beta(s) \cdot CF_{t+1}
         """)

st.write(r"""         where $\beta(s)$ is a sensitivity factor that captures how the cash flow changes in response to the climate scenario $s$, 
         and $CF_{t+1}$ is the cash flow in a baseline scenario (often referred to as the "no climate change" scenario).
         """)

st.write("""
         There are multiple limitations to this general approach,
         that prevent it from being of any use for an investor:
         """)

st.write(r"""
         1. Current approaches do not say anything about how to arrive to $P$, the unconditional price of the asset, which is what we need to value assets. To do 
         so, we need to assign probabilities to the scenarios.
         2. The discount rate $r_{t+1}$ is assumed constant across scenarios, which is a simplification that overlooks the state-dependent nature of risk and marginal value of money.
         """)

st.write("""
         This set the stage for large improvements in the way we value assets under climate risk. In this introduction, 
         we are going to progressively modify the initial equation to address these limitations, and arrive at a more comprehensive framework for asset pricing under climate risk.
         """)

st.subheader('The Need for Probabilistic Climate Scenarios')

st.write("""Prices reflect **expected discounted cash flows**:""")
st.latex(r'''
         P_t = \mathbb{E}_t\left( \frac{CF_{t+1}}{1 + r_{t+1}} \right)
         ''')


st.write("""
To arrive at the expected cash flow, we need to **assign probabilities** to the different states of the world:
         """)

st.latex(r'''
         \mathbb{E}_t\left( CF_{t+1} \right) = \sum_{s} \pi(s) CF(s)
         ''')


st.write("""
         where $\pi(s)$ is the probability of state $s$.
         """)

st.write("""In the section [Assigning Probabilities to Climate Scenarios](./Assigning_Probabilities_to_Climate_Scenarios), we will discuss how probabilities can 
         be assigned to abatement policies, and how these probabilities can be used to assign probabilities to climate scenarios.""")


st.write("""The main finding is that **most of the probability mass (90%) is concentrated on climate scenarios 
         with low or delayed abatement. Therefore, scenarios with 
         high physical damages are more likely to occur.**""")

st.write("""To see the impact 
         of this statement, let's have a simple example with a counterfactual cashflow of $100 and 
         a common decrease of 10% in the cashflow in a scenario with abatement but no physical damages and in a scenario with physical damages but no abatement.""")

st.write("""We assume a common discount rate of 5% in both scenarios.""")

st.write("""We assume 90% probability of the scenario with physical damages and 10% probability of the scenario with abatement.""")

st.write("""The relative contribution of each source of climate risk to the unconditional price of the asset is given by the following equation:""")

st.latex(r'''
         \text{Impact Physical Damages} = 0.9 \cdot \frac{100 - 90}{1 + 0.05} = 9.52
         ''')

st.latex(r'''
         \text{Impact Abatement} = 0.1 \cdot \frac{100 - 90}{1 + 0.05} = 0.95
         ''')

st.write("""Therefore, **most of the impact on the price of the asset comes from the scenario with high physical damages**, 
         which is the scenario with the highest probability. This highlights the importance of considering the probabilities of different scenarios when valuing assets under climate risk.""")

st.subheader("The Need for a State-Dependent Discount Factor")

st.write("""The price today should be **discounted by a state-dependent discount factor**, which reflects the risk associated with the cash flows in each scenario:""")

st.latex(r'''
         P_t = \mathbb{E}_t[ m_{t+1} \cdot CF_{t+1}]
         ''')

st.write("""where $m_{t+1}$ is the stochastic discount factor, which is a function of the state of the world at time $t+1$.""")
st.write("""The stochastic discount factor captures the risk preferences of investors and the state-dependent nature of the discount rate. That is,
         it reflects **how the marginal value of money changes across different states of the world**.""")

st.write("""Typically, you may value more future cash flows in bad states of the world, and less in good states of the world.
         This is because in bad states of the world, you may have a higher marginal utility of
         consumption, and therefore a higher marginal value of money. In good states of the world, you may have a lower marginal utility of consumption, and therefore a lower marginal value of money.""")

st.write("""In the section [State-Dependent Discount Factor](./State-Dependent_Discount_Factor), we will discuss how 
            the stochastic discount factor can be used to value assets under climate risk, and how the covariance between the cash flows of different assets and the stochastic discount factor can be used to adjust for risk.
            """)

st.write(r"""The main finding is that, **physical damages are expected to lower consumption growth (i.e. bad state of the world) while 
         high abatement are expected to occur in a state of high consumption growth (i.e. good state of the world)**. """)

st.write(r""" Therefore, **physical damages** are expected to occur with a **higher stochastic discount factor** while **abatement** is expected to occur with a **lower stochastic discount factor**.
         """)

st.write(r"""To see the impact of this statement on valuation, let's have a simple example with a counterfactual cashflow of $100 and 
         a common decrease of 10% in the cashflow in a scenario with abatement but no physical damages and in a scenario with physical damages but no abatement.""")

st.write(r"""We now have a higher stochastic discount factor in the scenario with high physical damages (1.10)
         and a lower stochastic discount factor in the scenario with abatement (0.90).""")

st.write(r"""We assume a 50/50 probability of the scenario with physical damages and the scenario with abatement.""")

st.write(r"""The relative contribution of each source of climate risk to the unconditional price of the asset is given by the following equation:""")

st.latex(r'''
            \text{Impact Physical Damages} = 0.5 \cdot 1.10 \cdot(100 - 90) = 5.50
            ''')

st.latex(r'''
            \text{Impact Abatement} = 0.5 \cdot 0.
90 \cdot (100 - 90)= 4.50
            ''')

st.write(r"""Therefore, **most of the impact on the price of the asset comes from the scenario with high physical damages**,
         which is the scenario with the highest stochastic discount factor. This highlights the importance of considering the
            stochastic discount factor when valuing assets under climate risk.""")

st.subheader("The Need for Spatial Finance")

st.write("""
So far, CIPs' modelling of the sensitivity factor $\\beta(s)$ has largely focused on **transition risks** — that is, how asset cash flows are impacted by different **abatement policies**, such as carbon taxes, regulatory changes, or technological transitions towards low-carbon alternatives.
""")

st.write("""
However, as demonstrated in our earlier examples, **physical damages** — such as those from extreme weather events, sea-level rise, or long-term temperature shifts — can have a **greater financial impact** on asset prices. In our first example, the scenario with **physical damages contributed more to the asset price** because it had a higher probability and occurred in a worse economic state.
""")

st.write("""
Unlike transition risks, **physical damages are inherently tied to location**. Flooding, heatwaves, hurricanes, droughts — these events impact **specific regions**, and their severity depends on **where the physical assets or economic activities are located**.
""")

st.write("""
This leads us to a key insight:  
**Valuing climate risk requires understanding where the asset is located.**
This is the core motivation for **spatial finance**.
""")

st.write("""
Spatial finance integrates **geographic data** (such as asset location, climate exposure maps, or hazard models) into the financial analysis. It allows investors to:
""")

st.markdown("""
- Assess **exposure to physical climate hazards** at the asset level.
- Understand how **regional climate impacts** translate into **cash flow risks**.
- Compare **regional resilience** and **adaptation capacity**.
- Incorporate **climate-adjusted risk premia** based on geographic vulnerability.
""")

st.write("""
For example, imagine two identical factories generating the same baseline cash flows, but one is located in a coastal flood zone and the other inland. Their **exposure to sea-level rise and storm surges** is radically different, and so is the expected impact on future cash flows.
""")

st.write("""
In the next section, [Modeling Physical Damages with Geo-Referenced Data](./Modeling_Physical_Damages_with_Geo_Referenced_Data), we will explore how to quantify these physical risks using location-based information, and how to integrate them into asset pricing models.
""")

st.write("""
The key takeaway is that **climate risk is not only about transition policies**, but also about **where the asset is located in the physical world**.  
Hence, understanding and pricing climate risk requires **spatially explicit models**.
""")
