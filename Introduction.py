import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px


st.title('Climate Risk and Asset Pricing')

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

st.write(r"""In most approaches, the sensitivity factor $\beta(s)$ is transition or physical risk specific, that is:
         """)

st.latex(r"""         \beta(s) = \begin{cases}
            \text{Transition Risk} & \text{if } s \text{ is a transition risk scenario} \\
            \text{Physical Risk} & \text{if } s \text{ is a physical risk scenario}
            \end{cases}
            """)

st.write(r"""In other words, the sensitivity factor $\beta(s)$ is traditionally to be specific to the type of climate risk scenario being considered, whether it is a transition risk scenario (e.g., a scenario where the world transitions to a low-carbon economy) or a physical risk scenario (e.g., a scenario where the world experiences significant physical impacts from climate change such as extreme weather events).
         In this context, transition and physical risks tend to be treated as **separate categories, each with its own set of scenarios and sensitivity factors**.
         The overall exposure of the asset to climate risks is then captured as:
         """)

st.latex(r"""
         \beta = \sum_s \beta(s)
            """)    

st.write(r"""With **the underlying assumption that none of the climate risks are priced in the market**, the potential misvaluation of the asset follows: 
         """)

st.latex(r"""
            \text{Repricing}= \frac{ \frac{\beta \cdot CF_{t+1}}{1 + r_{t+1}}}{\text{Market Price}} - 1
            """)

st.write("""
         There are multiple limitations to this general approach,
         that prevent it from being of any use for an investor:
         """)

st.write(r"""
         1. Current approaches do not say anything about how to arrive to $P$, the unconditional price of the asset, which is what we need to value assets. To do 
         so, we need to assign probabilities to the scenarios.
         2. The discount rate $r_{t+1}$ is assumed constant across scenarios, which is a simplification that overlooks the state-dependent nature of risk and marginal value of money.
         3. Considering physical and transition risks separately, as if they were independent, is a simplification that overlooks the interdependencies between these two types of risks.
         As a first order principle, the one depends intimately on the other. Modelling $\beta(s)$ separately for transition and physical risks ignores this intricacy.
         """)

st.write("""
         This set the stage for large improvements in the way we value assets under climate risk. In this introduction, 
         we are going to progressively modify the initial equation to address these limitations, and arrive at a more comprehensive framework for asset pricing under climate risk.
         """)

st.subheader('The Need for Probabilistic Climate Scenarios')

st.write("""
In finance, prices reflect **expected discounted cash flows**. These depend on outcomes across possible future states — and their **probabilities**.
These cash flows may take the form of dividends (for stocks), coupons (for bonds), or rental income (for real estate). 

Taking the expectations of the first equation, we can rewrite the price of an asset as:
""")

st.latex(r'''
P_t = \frac{\mathbb{E}_t\left( CF_{t+1} \right)}{1 + \mathbb{E}_t\left( r_{t+1} \right)}
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

st.write("""In the section [Assigning Probabilities to Climate Scenarios](./Assigning_Probabilities_to_Climate_Scenarios), we will discuss how probabilities can 
         be assigned to abatement policies, and how these probabilities can be used to assign probabilities to climate scenarios.""")

st.subheader("The Need for a State-Dependent Discount Rate")

st.write("""
So far, we have expressed asset prices as the present value of expected future cash flows, using a single discount rate that reflects time preference and some notion of risk.
But this is a simplification.
In reality, **different states of the world may bring not only different cash flows, but also different levels of risk and marginal value of money**.
""")

st.write("""
To properly capture this, we move from a single discount rate to a **state-dependent discounting** framework. This is done using what's called a 
**stochastic discount factor**, denoted by $m_{t+1}$. It tells us how much we value one unit of payoff in each possible future state - the higher the value of $m_{t+1}$, the more we value that unit of money in that state.         
""")


st.write("""
What does it means for an investor? Let's suppose we have two states of the world:
- one with low consumption (bad times) and 
- one with high consumption (good times). 
         
In this framework, the stochastic discount factor $m_{t+1}$ captures how much we value future cash flows in each state:
- in bad times, the marginal utility of consumption is high, meaning each additional unit of consumption is very valuable. 
- in good times, the marginal utility is lower.
                  """)

# Define states and values
states = ['Bad Times (Low Consumption)', 'Good Times (High Consumption)']
consumption = [1, 2]
marginal_utility = [1/c for c in consumption]
pricing_kernel = marginal_utility  # By theory, m_{t+1} ∝ u'(c_{t+1})

# Create a grouped bar chart
fig = go.Figure(data=[
    go.Bar(name='Consumption', x=states, y=consumption),
    go.Bar(name="SDF", x=states, y=pricing_kernel)
])

# Update layout
fig.update_layout(
    barmode='group',
    title="State-Dependent Values: Consumption and Stochastic Discount Factor",
    xaxis_title="State of the World",
    yaxis_title="Value",
    legend_title="Variables",
    template="plotly_white"
)

# Show in Streamlit
st.plotly_chart(fig)


st.write("""
With this, we can rewrite the asset pricing formula as:
""")

st.latex(r'''
P_t = \mathbb{E}_t \left[ m_{t+1} \cdot CF_{t+1} \right]
''')

st.write("""
This means that the price today is the expected value of the future cash flow, *weighted* by how valuable each unit of money is in the state in which it is received.
""")


st.write("""
This points out to a first inconsistency in the initial approach: **the discount rate is not constant across states of the world**.
         """)

st.write("""In our context of climate scenarios, this means that **the discount rate should be conditioned on the climate scenario, as the marginal utility of consumption may vary significantly across different scenarios**.
         """)


import plotly.graph_objects as go

# Climate scenarios
scenarios = ['Net Zero 2050', 'Current Policies', 'Hot House World']

# Assumed GDP/consumption levels (arbitrary illustrative values)
consumption = [1.8, 1.5, 1.0]  # GDP or consumption per capita proxy

# Stochastic Discount Factor (inverse of consumption)
sdf = [1 / c for c in consumption]

# Create grouped bar chart
fig = go.Figure(data=[
    go.Bar(name='Consumption (GDP proxy)', x=scenarios, y=consumption),
    go.Bar(name='Stochastic Discount Factor (SDF)', x=scenarios, y=sdf)
])

fig.update_layout(
    barmode='group',
    title='Climate Scenarios: GDP/Consumption vs. Stochastic Discount Factor',
    xaxis_title='Climate Scenario',
    yaxis_title='Value',
    legend_title='Variables',
    template='plotly_white'
)

st.plotly_chart(fig)


st.write("""
In fact, we should again refined our previous equation to account for the **covariance between the stochastic discount factor and the cash flow** of the asset:
""")

st.latex(r'''
P_t = \underbrace{\frac{\mathbb{E}_t(CF_{t+1})}{1 + r^f}}_{\text{Time discounting}} + \underbrace{\text{cov}_t(m_{t+1}, CF_{t+1})}_{\text{Risk adjustment}}
''')

st.write("""
If an asset pays off in bad states—when $m_{t+1}$ is high and consumption is low—then the covariance is positive, and the asset is **more valuable**. It acts like insurance.
Risky assets—those that pay more in good times—are discounted more heavily.
""")


st.write("""
To see this, let's assign a $1/2$ probability to two states of the world, one with a cash flow of $CF_u$ in good times and one with a cash flow of $CF_d$ in bad times.
We have fixed the stochastic discount factor to $m_u = 0.5$ in good times and $m_d = 1.0$ in bad times.
""")

# Toggle for scenario
scenario = st.radio(
    "",
    options=["Higher in good times", "Higher in bad times"]
)

# Fixed pricing kernel
m_u = 0.5  # low value in good times
m_d = 1.0  # high value in bad times

# Set CFs based on the toggle
if scenario == "Higher in good times":
    cf_u, cf_d = 2.0, 1.0
else:
    cf_u, cf_d = 1.0, 2.0

# Compute price
price = 0.5 * m_u * cf_u + 0.5 * m_d * cf_d

# Show setup
st.latex(r'''
P_t = \frac{1}{2} \cdot m_u \cdot CF_u + \frac{1}{2} \cdot m_d \cdot CF_d
''')
st.markdown(f"Where: \n- $CF_u = {cf_u}$, $CF_d = {cf_d}$")

# Show result
st.markdown(f"\n$P_t = {price:.2f}$")

st.write("""
Even though expected cash flow and volatility are the same, **the asset is worth more when it pays in bad times**, because cash flows are more valuable when $m_{t+1}$ is high (i.e., in bad states of the world).
""")

st.write("""
         In the context of climate risk, it means we should take into account how the cashflows of different assets may **covary** with climate risk.
         """)
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Time horizon
years = np.arange(2020, 2051)

# Simulated GDP loss path (% deviation from baseline)
gdp_loss = np.zeros_like(years, dtype=float)
gdp_loss[years >= 2030] = -0.1 * (years[years >= 2030] - 2030)  # e.g. -0.1% per year from 2030
gdp_loss = np.clip(gdp_loss, -5, 0)  # max 5% loss

# Normalize GDP loss (absolute value) for cashflow simulation
gdp_loss_abs = np.abs(gdp_loss)
gdp_loss_norm = (gdp_loss_abs - gdp_loss_abs.min()) / (gdp_loss_abs.max() - gdp_loss_abs.min())

# Simulate cashflows
cf_hedging = 1 + 0.5 * gdp_loss_norm   # pays more as GDP loss increases
cf_exposed = 1 - 0.5 * gdp_loss_norm   # pays less as GDP loss increases

# Create figure
fig = go.Figure()

# GDP loss curve
fig.add_trace(go.Scatter(
    x=years, y=gdp_loss,
    name="GDP Loss (%)",
    mode="lines",
    line=dict(color="black", dash="dot"),
    yaxis="y1"
))

# Hedging asset
fig.add_trace(go.Scatter(
    x=years, y=cf_hedging,
    name="Hedging Asset",
    mode="lines",
    line=dict(color="green"),
    yaxis="y2"
))

# Exposed asset
fig.add_trace(go.Scatter(
    x=years, y=cf_exposed,
    name="Exposed Asset",
    mode="lines",
    line=dict(color="brown"),
    yaxis="y2"
))

# Layout with dual y-axes
fig.update_layout(
    title="Cashflows under Climate-Driven GDP Loss",
    xaxis_title="Year",
    yaxis=dict(
        title="GDP Loss (%)",
        side="left",
        range=[-5.5, 0],
        showgrid=False
    ),
    yaxis2=dict(
        title="Asset Cashflows",
        overlaying="y",
        side="right",
        showgrid=True
    ),
    legend_title="",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.write("""In the section [State-Dependent Discount Rate](./State-Dependent_Discount_Rate), we will discuss how 
            the stochastic discount factor can be used to value assets under climate risk, and how the covariance between the cash flows of different assets and the stochastic discount factor can be used to adjust for risk.
            """)

st.subheader('The Need for an Integrated Approach')

st.write("""While general approaches tends to evaluate climate risks component separately, we find this approach to be simply inconsistent.
    """)

st.write("""
    To see this, let's start with a definition of transition costs as the economic costs needed to achieve a given level of decarbonization (emission reduction).
With this definition, it becomes clear that physical and transition costs are two sides of the same coin, since the greater the transition effort, 
the lower the global warming and resulting physical damages.
         """)

st.write(""" Therefore, a **state of the world $s$ that is characterized by a given level of transition costs will also be characterized by a level of physical damages**:
         """
)

# --- Interactive control
abatement = st.slider("", 0, 100, 50)

# --- Simple functional relationships
# Normalize abatement
abatement_fraction = abatement / 100

# Transition cost increases with abatement (convex relationship)
transition_cost = 2 * (abatement_fraction ** 2)  # max is 2% of GDP

# Physical damage decreases with abatement (concave relationship)
physical_damage = (1 - abatement_fraction) ** 2  # max is 1% of GDP

# Display outputs
col1, col2 = st.columns(2)
col1.metric("Transition Cost (% GDP)", f"{transition_cost:.2%}")
col2.metric("Physical Damages (% GDP)", f"{physical_damage:.2%}")

# --- Chart
fig = go.Figure()

x_vals = np.linspace(0, 1, 100)
fig.add_trace(go.Scatter(x=x_vals * 100, y=2 * (x_vals ** 2),
                         mode='lines', name='Transition Cost (% GDP)',
                         line=dict(color='blue')))
fig.add_trace(go.Scatter(x=x_vals * 100, y=(1 - x_vals) ** 2,
                         mode='lines', name='Physical Damage (% GDP)',
                         line=dict(color='red')))

fig.add_vline(x=abatement, line_width=2, line_dash="dash", line_color="gray")

fig.update_layout(
    title="Trade-off Between Transition Cost and Physical Damages",
    xaxis_title="Abatement Level (%)",
    yaxis_title="Cost (% of GDP)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.write(r"""An overall climate change sensitivity factor $\beta$ should not be the sum across the states of the world, 
         but the probability-weighted average of the sensitivity factors across the states of the world:
            """)

st.latex(r"""
         \beta = \sum_s \pi(s) \cdot \beta(s)
            """)

st.write(r"""The  potential misvaluation of the asset is then:""")

st.latex(r"""
            \text{Repricing}= \frac{ \frac{\sum_s \pi(s) \cdot \beta(s) \cdot CF_{t+1}}{1 + r_{t+1}}}{\text{Market Price}} - 1
                """)

st.write("""The implication for repricing is therefore that potential misvaluation of the asset is not the sum of the potential misvaluation due to impairements in 
         transition or physical risks-focused scenarios, but the probability-weighted average of the potential misvaluation across the states of the world.
            """)

st.write("""This points out to the inconsistency of the assumption that **none of the climate risks are priced in the market, 
         as it would imply that the market expects a high probability of a state of the world with no transition costs and no physical damages,
            which is not consistent with the current state of knowledge about climate change**.
            """)