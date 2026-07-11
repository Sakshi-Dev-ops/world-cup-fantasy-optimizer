import streamlit as st
import pandas as pd
import ctypes
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="World Cup Fantasy Optimizer", page_icon="⚽", layout="wide")
st.title("🏆 World Cup V7 Fantasy Optimization Engine")
st.markdown("Powered by an ultra-fast dynamic programming C++ backend algorithm.")

# --- CONNECT TO C++ BACKEND ---
class PlayerStruct(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 50),
        ("position", ctypes.c_char * 20),
        ("team", ctypes.c_char * 30),
        ("cost", ctypes.c_int),
        ("form_rating", ctypes.c_double),
        ("historical_points", ctypes.c_int)
    ]

# Automatic platform detection for compiled binaries
try:
    if os.name == 'nt':
        backend = ctypes.CDLL("./liboptimizer.dll")
    else:
        backend = ctypes.CDLL("./liboptimizer.so")
except Exception as e:
    st.error(f"⚠️ C++ library not found. Run the compilation command in your terminal first! Error: {e}")
    st.stop()

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

# --- RUN OPTIMIZATION ---
if st.button("🚀 Compute Globally Optimal Lineup"):
    player_array_type = PlayerStruct * len(df)
    c_players = player_array_type()
    
    for idx, row in df.iterrows():
        c_players[idx].name = row['name'].encode('utf-8')
        c_players[idx].position = row['position'].encode('utf-8')
        c_players[idx].team = row['team'].encode('utf-8')
        c_players[idx].cost = int(row['cost'])
        c_players[idx].form_rating = float(row['form_rating'])
        c_players[idx].historical_points = int(row['historical_points'])
        
    backend.optimize_lineup(c_players, len(df), budget_limit, team_cap)
    
    optimal_count = backend.get_optimal_count()
    optimized_list = []
    
    for i in range(optimal_count):
        out_p = PlayerStruct()
        backend.get_optimal_player(i, ctypes.byref(out_p))
        optimized_list.append({
            "Name": out_p.name.decode('utf-8'),
            "Position": out_p.position.decode('utf-8'),
            "Team": out_p.team.decode('utf-8'),
            "Cost ($M)": out_p.cost,
            "Form": out_p.form_rating,
            "History": out_p.historical_points
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
