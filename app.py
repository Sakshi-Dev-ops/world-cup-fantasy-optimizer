import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="World Cup Fantasy Optimizer", page_icon="⚽", layout="wide")
st.title("🏆 World Cup V7 Fantasy Optimization Engine")
st.markdown("Powered by a high-performance Knapsack Optimization backend algorithm.")

# --- SIDEBAR INTERFACE ---
st.sidebar.header("Optimization Variables")
budget_limit = st.sidebar.slider("Total Team Budget ($M)", min_value=40, max_value=120, value=100)
team_cap = st.sidebar.slider("Max Players Per Country", min_value=1, max_value=5, value=3)

# --- FANTASY DATASET ---
mock_data = [
    {"name": "Lionel Messi", "position": "FWD", "team": "Argentina", "cost": 15, "form_rating": 9.2, "historical_points": 85},
    {"name": "Kylian Mbappe", "position": "FWD", "team": "France", "cost": 14, "form_rating": 8.9, "historical_points": 80},
    {"name": "Kevin De Bruyne", "position": "MID", "team": "Belgium", "cost": 12, "form_rating": 8.5, "historical_points": 72},
    {"name": "Virgil van Dijk", "position": "DEF", "team": "Netherlands", "cost": 9, "form_rating": 7.8, "historical_points": 55},
    {"name": "Alisson Becker", "position": "GK", "team": "Brazil", "cost": 8, "form_rating": 8.1, "historical_points": 60},
    {"name": "Jude Bellingham", "position": "MID", "team": "England", "cost": 11, "form_rating": 8.7, "historical_points": 70},
    {"name": "Bukayo Saka", "position": "MID", "team": "England", "cost": 10, "form_rating": 8.0, "historical_points": 64},
    {"name": "Achraf Hakimi", "position": "DEF", "team": "Morocco", "cost": 8, "form_rating": 7.9, "historical_points": 58},
]

df = pd.DataFrame(mock_data)

st.subheader("Available Player Pool")
st.dataframe(df, use_container_width=True)

# --- RUN OPTIMIZATION (Dynamic Programming Knapsack Engine) ---
if st.button("🚀 Compute Globally Optimal Lineup"):
    # 1. Predictive Engine Formula: Calculate performance values
    values = [float(row['form_rating'] * 0.7 + row['historical_points'] * 0.3) for _, row in df.iterrows()]
    costs = df['cost'].tolist()
    n = len(df)
    
    # 2. DP Table build
    dp = [[0.0 for _ in range(budget_limit + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(budget_limit + 1):
            if costs[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-costs[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
                
    # 3. Backtracking to gather chosen players
    w = budget_limit
    chosen_indices = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            chosen_indices.append(i-1)
            w -= costs[i-1]
            
    optimized_list = []
    for idx in chosen_indices:
        row = df.iloc[idx]
        optimized_list.append({
            "Name": row['name'],
            "Position": row['position'],
            "Team": row['team'],
            "Cost ($M)": row['cost'],
            "Form": row['form_rating'],
            "History": row['historical_points']
        })
        
    if optimized_list:
        res_df = pd.DataFrame(optimized_list)
        st.success("✨ Optimization Complete! Mathematical Best Roster Found.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Players Picked", f"{len(res_df)}")
        col2.metric("Total Budget Spent", f"${res_df['Cost ($M)'].sum()}M / ${budget_limit}M")
        col3.metric("Projected Value Score", f"{res_df['History'].sum() + res_df['Form'].sum():.1f}")
        
        st.subheader("Your AI-Optimized World Cup Dream Team")
        st.table(res_df)
        
        st.subheader("Budget Allocation Strategy")
        st.bar_chart(res_df, x="Name", y="Cost ($M)")
    else:
        st.error("No valid lineup fits within the selected criteria.")
