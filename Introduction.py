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
However, as demonstrated in our earlier examples, **physical damages** can have a **greater financial impact** on asset prices. In our first example, even with a lower discount factor, the scenario with **physical damages contributed more to the asset price** because it had a higher probability and occurred in a worse economic state.
""")

st.write("""
Unlike transition risks, **physical damages are inherently tied to location**. Flooding, heatwaves, hurricanes, droughts — these events impact **specific areas**, and their severity depends on **where the physical assets or economic activities are located**.
""")

st.write("""
Therefore, **valuing climate risk requires understanding where the asset is located.** The state-dependent cashflows should therefore be modelled as:
""")

st.latex(r"""
         CF(s)_{t+1} = \beta(s_{lat,lon}) \cdot CF_{t+1}
         """)

st.write(r"""
where $s_{lat,lon}$ represents the climate scenario conditioned on the asset's geographic location (latitude and longitude), and $\beta(s_{lat,lon})$ is the sensitivity factor that captures how the cash flow changes in response to the climate scenario at that specific location.
         """)
# Create hypothetical data: locations and their beta sensitivity
geo_data = pd.DataFrame({
    'lat': [14.6, 40.7, -33.9, 1.3, 35.7, 
            19.4, 30.0, 51.5, -4.0, 23.1, 
            -1.3, 13.7, 28.6, -22.9, 34.0,
            31.2, 37.8, 39.9, 55.8, -17.7],
    'lon': [-61.0, -74.0, 151.2, 103.8, 139.7, 
            -99.1, 120.9, -0.1, 39.7, 113.3, 
            36.8, 100.5, 77.2, -43.2, -6.8,
            121.5, -122.4, 116.4, 37.6, 178.4],
    'City': ['Caribbean', 'New York', 'Sydney', 'Singapore', 'Tokyo', 
             'Mexico City', 'Shanghai', 'London', 'Dar es Salaam', 'Guangzhou', 
             'Nairobi', 'Bangkok', 'Delhi', 'Rio de Janeiro', 'Tunis',
             'Manila', 'San Francisco', 'Beijing', 'Moscow', 'Fiji'],
    'Beta Sensitivity': [0.55, 0.2, 0.35, 0.4, 0.15,
                         0.3, 0.45, 0.1, 0.5, 0.6,
                         0.4, 0.5, 0.3, 0.5, 0.25,
                         0.65, 0.2, 0.3, 0.1, 0.6]
})


fig = px.scatter_mapbox(
    geo_data,
    lat="lat",
    lon="lon",
    color="Beta Sensitivity",
    size="Beta Sensitivity",
    hover_name="City",
    color_continuous_scale="YlOrRd",
    size_max=30,
    zoom=1,
    height=500
)

fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)