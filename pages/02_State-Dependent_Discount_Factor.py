import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("State-Dependent Discount Factor")

st.write(r"""We describe what the investor wants by a **utility function**:
""")

st.latex(r"""
U(c, c_{t+1}) = u(c_t) + \beta \mathbb{E}[u(c_{t+1})]
""")

st.write(r"""where $c_t$ is the consumption at time $t$, $c_{t+1}$ is the consumption at time $t+1$, $\beta$ is a time preference factor.
         """)

st.write(r"""
         The point of a utility function is to capture investor's aversion to **risk** and **delay**, and appropriately discount prices.
         The utility function gives us a good way of seeing how impatience and risk aversion impact asset prices.""")

st.write(r"""
An example is the log utility function:
""")

st.latex(r"""
u(c) = \log(c); \quad u'(c) = \frac{1}{c} 
""")


# Define consumption range
c = np.linspace(0.1, 3, 500)
u_c = np.log(c)
u_prime_c = 1 / c

# Create log utility function chart
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=c, y=u_c, mode='lines', name='u(c) = log(c)'))
fig1.update_layout(title='Log Utility Function', xaxis_title='Consumption (c)', yaxis_title='Utility')

# Create marginal utility function chart
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=c, y=u_prime_c, mode='lines', name="u'(c) = 1/c"))
fig2.update_layout(title='Marginal Utility Function', xaxis_title='Consumption (c)', yaxis_title='Marginal Utility')


st.write(r"""The utility level $u(c)$ is the satisfaction or **happiness** that the investor derives from consuming $c$.
         """)
# Display charts in Streamlit
st.plotly_chart(fig1)

st.write(r"""The marginal utility $u'(c)$ is the **additional satisfaction** or happiness that the investor derives from **consuming an additional unit of $c$**.
         It is the slope of the utility function at a given point. 
         At any point on the x-axis, the y-axis tells you how much extra happiness you get from consuming one more unit at that level.
The more you already consume, the less valuable one more unit becomes.""")

st.plotly_chart(fig2)

st.write(r"""
         A more useful functional form generalizes log: it lets us adjust the **curvature of the utility function (i.e., risk aversion)**:
""")

st.latex(r"""
u(c) = \frac{c^{1-\gamma}}{1-\gamma}; \quad u'(c) = c^{-\gamma}
""")

st.write(r"""
The coefficient of relative risk aversion (CRRA), denoted by $\gamma$, determines the curvature of the utility function. 
It reflects **how strongly the investor dislikes risk and how unwilling they are to shift consumption across time**. 
A **higher $\gamma$ means greater risk aversion** — the utility function becomes steeper, and the investor places 
less value on additional consumption when they already have a lot.

The CRRA marginal utility curves show how quickly the value of extra consumption declines as total consumption increases. 
With a high $\gamma$, the investor effectively says, *"I already have enough — getting more doesn't add much value."* 
This behavior plays a key role in how future, risky payoffs are valued in asset pricing.
""")

# Gamma values to plot
gamma_values = [0.5, 1, 2, 5, 20]

# Plotly figure for utility
fig_utility = go.Figure()
for gamma in gamma_values:
    if gamma == 1:
        u_c = np.log(c)
    else:
        u_c = (c ** (1 - gamma)) / (1 - gamma) 
    fig_utility.add_trace(go.Scatter(x=c, y=u_c, mode='lines', name=f'γ = {gamma}'))

fig_utility.update_layout(
    title="CRRA Utility Function",
    xaxis_title="Consumption (c)",
    yaxis_title="Utility u(c)",
    yaxis_range=[-5, 5]
)

# Plotly figure for marginal utility
fig_marginal = go.Figure()
for gamma in gamma_values:
    u_prime_c = c ** (-gamma)
    fig_marginal.add_trace(go.Scatter(x=c, y=u_prime_c, mode='lines', name=f'γ = {gamma}'))

fig_marginal.update_layout(
    title="CRRA Marginal Utility Function",
    xaxis_title="Consumption (c)",
    yaxis_title="Marginal Utility u'(c)",
    yaxis_range=[0, 3]
)
# Display charts in Streamlit
st.plotly_chart(fig_marginal)


st.write(r"""
Now, what is the value of a cashflow $CF_{t+1}$ to an investor with a utility function $u(c_t) + \beta \mathbb{E}[u(c_{t+1})]$ at time $t$?     
The investor sits at this level of utility:
         """)

st.latex(r"""
         U_{\text{before}} = u(c_t) + \beta \mathbb{E}[u(c_{t+1})]
""")

st.write(r"""if you buy $\zeta$ more shares, you lose $p_t \zeta$ today, but you gain $CF_{t+1} \zeta$ tomorrow, so""")

st.latex(r"""
            U_{\text{after}} = \underbrace{u(c_t - p_t \zeta)}_{\text{today}} + \underbrace{\beta \mathbb{E}[u(c_{t+1} + CF_{t+1} \zeta)]}_{\text{tomorrow}}
""")

st.latex(r"""
            U_{\text{after}} = \underbrace{u(c_t) - u'(c_t) p_t \zeta}_{\text{today}} + \underbrace{\beta \mathbb{E}[u(c_{t+1}) + u'(c_{t+1}) CF_{t+1} \zeta)]}_{\text{tomorrow}}
""")


st.write(r"""The increase in utility is the difference between the two:
""")

st.latex(r"""
         U_{\text{after}} - U_{\text{before}} = -u'(c_t) p_t \zeta + \beta \mathbb{E}[u'(c_{t+1}) CF_{t+1} \zeta]
""")

st.write(r"""The investor will buy the shares as long as the increase in utility is positive, i.e.,""")

st.latex(r"""
            -u'(c_t) p_t + \beta \mathbb{E}[u'(c_{t+1})CF_{t+1}] = 0
         """)

st.write(r"""This gives us the **equilibrium price** of the asset:""")
st.latex(r"""
            P_t = \beta \mathbb{E}[\frac{u'(c_{t+1})}{u'(c_t)} CF_{t+1}]
         """)

st.write(r"""
         It's useful to separate:""")

st.latex(r"""
         m_{t+1} = \beta \frac{u'(c_{t+1})}{u'(c_t)}
         """)

st.write(r"""This is the **stochastic discount factor** that captures how the investor's risk aversion and consumption growth affect the value of future payoffs.
         It adjusts the discount rate based on the investor's current consumption and expected future consumption growth.""")


st.write(r"""The price of the asset can then be expressed as:""")
st.latex(r"""
            P_t = \mathbb{E}_t[m_{t+1}CF_{t+1}]
            """)



st.write(r"""
         Using the CRRA utility function, we have:""")

st.latex(r"""
         m_{t+1} = \beta \left(\frac{c_{t+1}}{c_t}\right)^{-\gamma}
         """)




st.latex(r"""m_{t+1} \approx 1 - \delta - \gamma \Delta c_{t+1}""")

# Interpretation
st.write(r"""
The stochastic discount factor $m_{t+1}$ tells us how much the investor values a future payoff in state $t+1$.  
- When **consumption growth increases** (i.e., times are good), $m_{t+1}$ **decreases**, meaning future payoffs are **less valuable**.
- When **consumption growth decreases** (i.e., times are bad), $m_{t+1}$ **increases**, meaning future payoffs are **more valuable**.

This captures **risk aversion**: investors value payoffs more in bad times.
""")
# Fixed parameters
delta = 0.03
gamma = 2.0

# User input: consumption growth
delta_c = st.slider("Consumption growth (Δcₜ₊₁)", min_value=-0.1, max_value=0.1, value=0.02, step=0.01)

# Compute m_{t+1}
m_approx = 1 - delta - gamma * delta_c

# Display computation
st.latex(rf"m_{{t+1}} \approx 1 - {delta} - {gamma} \times {delta_c} = {m_approx:.3f}")


st.subheader("Risk-free Rate")

st.write(r"""The risk-free rate is the return on a risk-free asset, such as government bonds. Assuming we pay 1 dollar today to obtain $R^f$:""")

st.latex(r"""1 = \mathbb{E}_t[m_{t+1} R^f] = \mathbb{E}_t[m_{t+1}] R^f """)

st.latex(r"""R^f = \frac{1}{\mathbb{E}_t[m_{t+1}]}""")

st.write(r"""Then:""")

st.latex(r"""R^f = \frac{1}{\beta} \left(\frac{c_t}{\mathbb{E}_t[c_{t+1}]}\right)^{-\gamma}""")

st.latex(r"""R^f \approx 1 + \delta + \gamma \mathbb{E}_t [\Delta c_{t+1}]""")

st.write(r"""We see that it depends on the expected consumption growth, the investor's risk aversion and impatience of investors. **Higher consumption growth leads to higher risk-free rate.
         Lower consumption growth leads to lower risk-free rate.**""")

# Parameters
delta = 0.02
gamma = 2.0

# Define a range of expected consumption growth values
expected_dc = np.linspace(-0.05, 0.05, 500)

# Compute risk-free rate using the approximation
rf_rate = 1 + delta + gamma * expected_dc

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=expected_dc, y=rf_rate, mode='lines', name=r"$R^f_t$"))
fig.update_layout(
    title="Risk-Free Rate vs. Expected Consumption Growth",
    xaxis_title=r"Expected Consumption Growth",
    yaxis_title=r"Risk-Free Rate",
    showlegend=False
)

st.plotly_chart(fig)


fig_dam = go.Figure()
fig_dam.add_trace(go.Scatter(x=expected_dc, y=rf_rate, mode='lines', name=r"$R^f_t$"))

# Add annotations for physical damages and abatement
fig_dam.add_vline(x=-0.03, line=dict(color='red', dash='dash'), name='Physical Damages')
fig_dam.add_annotation(x=-0.03, y=1 + delta + gamma * (-0.03), text="Physical Damages\n↓ consumption growth\n↓ Risk-Free Rate", 
                   showarrow=True, arrowhead=1, ax=-60, ay=40, bgcolor='white')

fig_dam.add_vline(x=0.03, line=dict(color='green', dash='dash'), name='Abatement in Good Times')
fig_dam.add_annotation(x=0.03, y=1 + delta + gamma * (0.03), text="Abatement\n↑ consumption growth\n↑ Risk-Free Rate", 
                   showarrow=True, arrowhead=1, ax=60, ay=-40, bgcolor='white')

# Final chart formatting
fig_dam.update_layout(
    title="Risk-Free Rate Response to Expected Consumption Growth",
    xaxis_title=r"Expected Consumption Growth",
    yaxis_title=r"Risk-Free Rate",
    showlegend=False
)

st.write("""So, what does it means in the context of climate change?
**Physical damages are expected to lower consumption growth, 
         so we expect lower risk-free rate.**
**Abatement is expected to be higher in good times,
         so we expect higher risk-free rate.**""")

st.plotly_chart(fig_dam)

st.write(r"""What does it implies for valuation of assets? It means that **physical damages** will **impact more the valuation of risky assets than abatement**, 
         because physical damages are expected to lower consumption growth, which leads to lower risk-free rate (i.e., lower discounting of future cash flows),
         while abatement is expected to increase consumption growth, which leads to higher risk-free rate (i.e., higher discounting of future cash flows).
         """)


st.subheader("Risk Premium")

st.write(r"""Now how to value risky assets?""")

st.write(r"""We use the definition of covariance:""")

st.latex(r"""Cov(m_{t+1}, CF_{t+1}) = \mathbb{E}_t[m_{t+1} CF_{t+1}] - \mathbb{E}_t[m_{t+1}] \mathbb{E}_t[CF_{t+1}]""")

st.write(r"""Then:""")

st.latex(r"""P_t = \mathbb{E}_t[m_{t+1} CF_{t+1}] = \mathbb{E}_t[m_{t+1}] \mathbb{E}_t[CF_{t+1}] + Cov(m_{t+1}, CF_{t+1})""")

st.latex(r"""P_t = \frac{1}{R^f} \mathbb{E}_t[CF_{t+1}] + Cov(m_{t+1}, CF_{t+1})""")

st.write(r"""With the approximation:""")

st.latex(r"""m_{t+1} \approx 1 - \delta - \gamma \Delta c_{t+1}""")

st.write(r"""We have:""")

st.latex(r"""Cov(m_{t+1}, CF_{t+1}) \approx -\gamma Cov(\Delta c_{t+1}, CF_{t+1})""")

st.write(r"""So the price of the asset is:""")

st.latex(r"""P_t \approx \underbrace{\frac{1}{R^f} \mathbb{E}_t[CF_{t+1}]}_{\text{Present Value (Time)}} - \underbrace{\gamma Cov(\Delta c_{t+1}, CF_{t+1})}_{\text{Risk Premium}}""")


st.write("""
If an asset pays off in bad states—when $m_{t+1}$ is high and consumption is low—then the covariance is positive, and the asset is **more valuable**. It acts like insurance.
Risky assets—those that pay more in good times—are discounted more heavily.
""")

st.write("""
Suppose there are two possible states of the world tomorrow, each equally likely.
An asset pays a cash flow $CF_{t+1}$ that depends on the state:
""")

scenario = st.radio(
    "Choose the asset type:",
    options=["Pays more in good times", "Pays more in bad times"]
)

# Fixed pricing kernel
m_u = 0.5  # good times → low marginal utility
m_d = 1.0  # bad times → high marginal utility

# Risk-free rate: E[m] = 0.5*(m_u + m_d)
rf_inverse = 1 / (0.5 * (m_u + m_d))

# Set cash flows
if scenario == "Pays more in good times":
    x_u, x_d = 2.0, 1.0
else:
    x_u, x_d = 1.0, 2.0

# Expected payoff
expected_x = 0.5 * (x_u + x_d)

# Expected m
expected_m = 0.5 * (m_u + m_d)

# Asset price
price = 0.5 * m_u * x_u + 0.5 * m_d * x_d

# Implied return
expected_return = expected_x / price
risk_premium = expected_return - rf_inverse

# Show setup
st.latex(r'''
P_t = \mathbb{E}[m_{t+1} CF_{t+1}] = \frac{1}{2} m_u CF_{u} + \frac{1}{2} m_d CF_d
''')
st.markdown(f"- $CF_u = {x_u}$, $CF_d = {x_d}$  \n- $m_u = {m_u}$, $m_d = {m_d}$")

st.latex(f"\\mathbb{{E}}[CF_{{t+1}}] = {expected_x:.2f} \\quad \\text{{ and }} \\quad p_t = {price:.2f}")

st.latex(f"\\text{{Expected return}} = \\frac{{\\mathbb{{E}}[CF_{{t+1}}]}}{{p_t}} = {expected_return:.2f}")
st.latex(f"\\text{{Risk-free rate}} = R^f = {rf_inverse:.2f}")
st.latex(f"\\textbf{{Risk premium}} = {expected_return:.2f} - {rf_inverse:.2f} = {risk_premium:.2f}")

if scenario == "Pays more in bad times":
    st.success("This asset pays off in bad states → negative covariance with $m_{t+1}$ → **lower risk premium** → **higher price**.")
else:
    st.error("This asset pays off in good states → positive covariance with $m_{t+1}$ → **higher risk premium** → **lower price**.")

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
