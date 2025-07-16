import streamlit as st
import plotly.graph_objects as go
import polars as pl
from scipy.stats import gaussian_kde
import numpy as np

st.title("Assigning Probabilities to Climate Scenarios")


st.write("""
In finance, prices reflect **expected discounted cash flows**. These depend on outcomes across possible future states — and their **probabilities**.
These cash flows may take the form of dividends (for stocks), coupons (for bonds), or rental income (for real estate). 

Taking the expectations of the first equation, we can rewrite the price of an asset as:
""")

st.latex(r'''
P_t = \mathbb{E}_t[\frac{CF_{t+1}}{1 + r_{t+1}}]
''')

st.write("""
where $P_t$ is the current price, $CF_{t+1}$ is the cash flow received at time $t+1$, and $r_{t+1}$ is the discount rate applicable at that time.
""")

st.write("""
To arrive at the expected cash flow, we need to assign probabilities to the different states of the world:
         """)

st.latex(r'''
         \mathbb{E}_t\left( CF_{t+1} \right) = \sum_{s} \pi(s) CF(s)
         ''')


st.write("""
         where $\pi(s)$ is the probability of state $s$.
         """)



# Fixed scenario assumptions
cf_a = 100.0  # Cash Flow in Green Transition
r_a = 0.05    # Discount Rate in Green Transition (5%)

cf_b = 50.0   # Cash Flow in Delayed Transition
r_b = 0.10    # Discount Rate in Delayed Transition (10%)

# Interactive slider for probability of State A
prob_a = st.slider("Probability of State A", 0.0, 1.0, 0.5)
prob_b = 1.0 - prob_a

# Expected values
expected_cf = prob_a * cf_a + prob_b * cf_b
expected_r = prob_a * r_a + prob_b * r_b
price = expected_cf / (1 + expected_r)

# Show setup
st.latex(r'''
\mathbb{E}_t(CF_{t+1}) = \pi_A \cdot CF_A + \pi_B \cdot CF_B
''')
# Show setup
st.latex(r'''
\mathbb{E}_t(r_{t+1}) = \pi_A \cdot r_A + \pi_B \cdot r_B
''')
st.markdown(f"Where:  \n- $CF_A = {cf_a}$, $r_A = {r_a}$  \n- $CF_B = {cf_b}$, $r_B = {r_b}$  \n- $\pi_A = {prob_a:.2f}$, $\pi_B = {prob_b:.2f}$")

# Show result
st.markdown(f"\n$P_t = {price:.2f}$")

st.write("""
         In the context of climate risk, states of the world can be defined by different climate scenarios, leading to different outcomes 
         such as temperature changes, policy responses, and economic impacts.""")

import plotly.graph_objects as go

# Simulated years
years = list(range(2020, 2101, 10))

# Simulated data for temperature (°C above pre-industrial)
temperature_paths = {
    'Net Zero 2050':     [1.2, 1.3, 1.4, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
    'Current Policies':  [1.2, 1.4, 1.6, 1.9, 2.2, 2.5, 2.8, 3.0, 3.2],
    'Delayed Transition': [1.2, 1.4, 1.7, 2.0, 2.4, 2.7, 2.9, 3.0, 3.1],
    'Hot House World':   [1.2, 1.5, 1.9, 2.4, 2.9, 3.4, 3.9, 4.3, 4.7],
}

# Simulated data for emissions (GtCO₂/year)
emissions_paths = {
    'Net Zero 2050':     [35, 30, 22, 15, 8, 2, 0, 0, 0],
    'Current Policies':  [35, 36, 37, 38, 39, 40, 41, 42, 43],
    'Delayed Transition': [35, 36, 35, 30, 25, 18, 10, 5, 0],
    'Hot House World':   [35, 38, 42, 45, 47, 49, 50, 51, 52],
}

# Simulated GDP loss (% deviation from baseline)
gdp_paths = {
    'Net Zero 2050':     [0, -0.2, -0.4, -0.6, -0.8, -1.0, -1.2, -1.3, -1.4],
    'Current Policies':  [0, -0.1, -0.3, -0.7, -1.2, -1.8, -2.5, -3.3, -4.0],
    'Delayed Transition': [0, -0.2, -0.5, -1.0, -1.7, -2.4, -3.1, -3.8, -4.5],
    'Hot House World':   [0, -0.3, -0.8, -1.6, -2.6, -3.7, -5.0, -6.4, -7.9],
}

# Plot 1: Temperature pathways
fig_temp = go.Figure()
for scenario, temps in temperature_paths.items():
    fig_temp.add_trace(go.Scatter(x=years, y=temps, mode='lines', name=scenario))
fig_temp.update_layout(
    title="Temperature Increase by Scenario (°C above pre-industrial)",
    xaxis_title="Year",
    yaxis_title="Temperature (°C)",
    template="plotly_white"
)
st.plotly_chart(fig_temp, use_container_width=True)

# Plot 2: Emissions pathways
fig_emiss = go.Figure()
for scenario, emissions in emissions_paths.items():
    fig_emiss.add_trace(go.Scatter(x=years, y=emissions, mode='lines', name=scenario))
fig_emiss.update_layout(
    title="CO₂ Emissions by Scenario (GtCO₂/year)",
    xaxis_title="Year",
    yaxis_title="Emissions (GtCO₂/year)",
    template="plotly_white"
)
st.plotly_chart(fig_emiss, use_container_width=True)

# Plot 3: GDP deviation
fig_gdp = go.Figure()
for scenario, gdp_losses in gdp_paths.items():
    fig_gdp.add_trace(go.Scatter(x=years, y=gdp_losses, mode='lines', name=scenario))
fig_gdp.update_layout(
    title="GDP Loss Relative to Baseline (%)",
    xaxis_title="Year",
    yaxis_title="GDP Loss (%)",
    template="plotly_white"
)
st.plotly_chart(fig_gdp, use_container_width=True)

st.write("""Much has been written on the construction and features of theses scenarios, but for the purpose of our discussion, the most 
         important feature is that, by design, they have not been associated any probabilistic estimate. We claim that, for 
         these scenarios to be of use, at least an **order-of-magnitude estimate of their likelihood must be provided**.
         """)

st.write("""
        Two sets of objections are normally raised against the feasibility of, or even the need for, a probabilistic characterization of scenarios:
         
         1. The first points to the difficulty in assigning probabilities to quantities that depend, among other things, on difficult-to-quantify policy choices.
         2. The second is based on the observation that financial scenarios are often prescribed without any probabilities attached to them, and that 
         climate scenarios as well can therefore be formulated in this probability-agnostic mannner.
         """)

st.write(""" Regarding the first objection, we are aware of, and will discuss in the corresponding section, the great challenges that come 
         with a probabilistic quantification of policy choices. **We find it difficult to accept, however, that a totally diffuse prior - one that 
         effectively assigns identical likelihood to any climate outcome - is the best description of our state of knowledge about how the climate / economy will evolve**.
         """)

st.write("""
         Regarding the second objection, it must be stressed that **climate and financial scenarios are intrisically different**: when we assign a market or credit scenario,
         we can, formally or informally, rely on at least a hundred-year history of financial crises, changing economic regimes and various combinations of 
         financial and economic occurences. Thanks to this wealth of data, a formal probabilistic assessment of the severity of a given financial scenario can be 
         obtained using traditional econometric techniques. Even when this is not done, thanks to a body of background expert knowledge and informal 
         mental assessments of the scenario likelihood is implicitly carried out by the professional users of market scenarios.
         """)

st.write("""
         The situation is radically different in the case of climate scenarios, because, when it comes to climate outcomes, we 
         simply do no not have the wealth of information that has been collected in the financial domain.
         This, of course, is because so far we have only experienced a modest average temperature anomaly between 1.1 and 1.4°C, and the associated damages 
         have been limited an manageable. We expect these temperatuer increases to be greatly exceeded by the end of the century, and perhaps much earlier, but do 
         not have even an intuitive feel for the relative probability of the different temperature outcomes. To bring the point home forcefully,
         the human species, let alone financial markets, have never experienced temperature anomalies of 3°C, and there are many emission trajectories that 
         bring us close or beyond this temperature.""")


st.subheader("Social Cost of Carbon (SCC)")


st.subheader("The Relationship Between SCC and Abatement")