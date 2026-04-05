



import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Fake News Spread Model", layout="centered")

st.title("📰 Fake News Spread Modelling")

# -----------------------------
# THEORY (DETAILED)
# -----------------------------
st.header("📘 Theory: Fake News Spread & SIR Model")

st.markdown("""
Fake news spread modelling is inspired by the **SIR (Susceptible–Infected–Recovered) model**, 
which is widely used in epidemiology to study how diseases spread in a population.

### 🔬 SIR Model Concept:
- **S (Susceptible)** → People who can get infected  
- **I (Infected)** → People who are infected and spreading  
- **R (Recovered)** → People who recovered and are immune  

### 📰 Mapping to Fake News:
We adapt this model to social media:

- **S (Skeptic)** → Users who have not believed the news yet  
- **B (Believer)** → Users who believe and spread fake news  
- **F (Fact-checker)** → Users who verify and stop spreading  

### ⚙️ Working Mechanism:
- A **Believer (B)** interacts with neighbors in a social network  
- If a neighbor is a Skeptic (S), they may become Believer with probability **β (Beta)**  
- A Believer may become Fact-checker (F) with probability **γ (Gamma)**  

### 📊 Importance:
- Helps understand how misinformation spreads  
- Shows impact of fact-checking  
- Useful in controlling fake news on social media  

### 📈 Visualization:
- **Line Graph** → Shows how users change over time  
- **Bar Chart** → Shows final distribution  
""")

# -----------------------------
# INPUT
# -----------------------------
st.header("⚙️ Enter Inputs")

try:
    N = int(st.text_input("Number of Users", "100"))
    prob = float(st.text_input("Connection Probability (0-1)", "0.05"))
    beta = float(st.text_input("Spread Rate (Beta)", "0.6"))
    gamma = float(st.text_input("Fact-check Rate (Gamma)", "0.1"))
    time_steps = int(st.text_input("Time Steps", "30"))
    initial_b = int(st.text_input("Initial Believers", "10"))

    valid = True
except:
    st.error("⚠️ Please enter valid numeric values!")
    valid = False

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation") and valid:

    random.seed(42)

    G = nx.erdos_renyi_graph(N, prob)

    states = {node: 'S' for node in G.nodes()}
    initial_believers = random.sample(list(G.nodes()), min(initial_b, N))

    for node in initial_believers:
        states[node] = 'B'

    believers, skeptics, fact_checkers = [], [], []

    for t in range(time_steps):
        new_states = states.copy()

        for node in G.nodes():
            if states[node] == 'B':

                for neighbor in G.neighbors(node):
                    if states[neighbor] == 'S' and random.random() < beta:
                        new_states[neighbor] = 'B'

                if random.random() < gamma:
                    new_states[node] = 'F'

        states = new_states

        believers.append(sum(1 for s in states.values() if s == 'B'))
        skeptics.append(sum(1 for s in states.values() if s == 'S'))
        fact_checkers.append(sum(1 for s in states.values() if s == 'F'))

    # -----------------------------
    # OUTPUT TABLE
    # -----------------------------
    st.header("📋 Output Data")

    df = pd.DataFrame({
        "Time": list(range(time_steps)),
        "Believers": believers,
        "Skeptics": skeptics,
        "Fact-checkers": fact_checkers
    })

    st.dataframe(df)

    # -----------------------------
    # LINE GRAPH
    # -----------------------------
    st.header("📈 Graph")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(believers, linewidth=2, label="Believers")
    ax.plot(skeptics, linewidth=2, linestyle='--', label="Skeptics")
    ax.plot(fact_checkers, linewidth=2, linestyle='-.', label="Fact-checkers")

    ax.set_xlabel("Time Steps")
    ax.set_ylabel("Number of Users")
    ax.set_title("Fake News Spread Over Time")

    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    plt.tight_layout()
    st.pyplot(fig)

    # -----------------------------
    # BAR CHART
    # -----------------------------
    st.header("📊 Final Comparison")

    final_values = [believers[-1], skeptics[-1], fact_checkers[-1]]
    categories = ["Believers", "Skeptics", "Fact-checkers"]

    fig2, ax2 = plt.subplots(figsize=(6, 4))

    ax2.bar(categories, final_values)

    for i, v in enumerate(final_values):
        ax2.text(i, v + 1, str(v), ha='center')

    ax2.set_ylabel("Users")
    ax2.set_title("Final State Distribution")

    plt.tight_layout()
    st.pyplot(fig2)

    # -----------------------------
    # EXPLANATION
    # -----------------------------
    st.header("🧠 Explanation")

    st.write(f"""
    - Initial Believers: {initial_b}
    - Beta (Spread Rate): {beta}
    - Gamma (Fact-check Rate): {gamma}

    ### 📌 Observations:
    - When **Beta > Gamma**, fake news spreads rapidly  
    - When **Gamma increases**, fake news gets controlled  
    - Skeptics decrease as they convert to Believers  

    ### 📊 Final Result:
    - Believers: {believers[-1]}
    - Skeptics: {skeptics[-1]}
    - Fact-checkers: {fact_checkers[-1]}
    """)
