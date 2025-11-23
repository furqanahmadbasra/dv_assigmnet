



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import parallel_coordinates


import os
import pandas as pd



csv_url = "https://drive.google.com/uc?export=download&id=1D12vfWH1zMaSnlr7UOgfWdD6zVJlVu5F"

df = pd.read_csv(csv_url)


st.markdown(
    '<h1 style="text-align: center; color: red;">Furqan Ahmad Basra (CS13C)</h1>',
    unsafe_allow_html=True
)

st.title("Sports Performance Dashboard")
st.write("Visualizations based on Cleaned Excel Data")


st.subheader("Parallel Coordinates Plot")

pcs_cols = [
    "Game Prestige Score",
    "Group1", "Group2", "Group3", "Group4",
    "PK", "IND", "IR", "CN", "UK", "GER", "AUS", "CAN", "USA"
]

pcs_df = df[pcs_cols].copy()

prestige_norm = (
    pcs_df["Game Prestige Score"] - pcs_df["Game Prestige Score"].min()
) / (pcs_df["Game Prestige Score"].max() - pcs_df["Game Prestige Score"].min())

pcs_df["PrestigeColor"] = prestige_norm
pcs_df["PrestigeBucket"] = pd.qcut(
    prestige_norm, 5,
    labels=["Very Low", "Low", "Medium", "High", "Very High"]
)

cmap = plt.cm.plasma
unique_labels = pcs_df["PrestigeBucket"].unique()
color_map = {
    label: cmap(i / (len(unique_labels) - 1))
    for i, label in enumerate(unique_labels)
}

fig1 = plt.figure(figsize=(50, 20), dpi=160)

parallel_coordinates(
    pcs_df.drop(columns=["PrestigeColor"]),
    class_column="PrestigeBucket",
    color=[color_map[label] for label in unique_labels],
    alpha=0.5,
    linewidth=2.5
)

plt.legend(fontsize=26)
plt.title(
    "Parallel Coordinates Plot: Groups + Countries (Colored by Prestige Score)",
    fontsize=32,
    pad=25
)
plt.ylabel("Value Scale", fontsize=24)
plt.xticks(rotation=45, fontsize=26)
plt.yticks(fontsize=22)
plt.grid(True, alpha=0.25)

st.pyplot(fig1)















st.subheader("Scatter Plot: Prestige vs Total Medals")

country_cols = ["PK", "IND", "IR", "CN", "UK", "GER", "AUS", "CAN", "USA"]
selected_country = st.selectbox("Select Country for Medal Coloring", country_cols)

fig2 = plt.figure(figsize=(12, 7))

df["Group_Total"] = df["Group1"] + df["Group2"] + df["Group3"] + df["Group4"]

sns.scatterplot(
    x="Game Prestige Score",
    y="Total Medals",
    size="Group_Total",
    hue=selected_country,       
    data=df,
    sizes=(20, 600),
    alpha=0.7,
    palette="plasma"
)

plt.title(f"Prestige vs Total Medals (Colored by {selected_country} Performance)")
plt.xlabel("Game Prestige Score")
plt.ylabel("Total Medals")
plt.legend(
    title=f"{selected_country} Medals",
    title_fontsize=14,
    fontsize=12,
    bbox_to_anchor=(1.05, 1),
    loc='upper left'
)

st.pyplot(fig2)










st.subheader("Line Plot: Pakistan vs Group1 Performance Across Prestige Levels")

df_sorted = df.sort_values("Game Prestige Score")

fig3 = plt.figure(figsize=(14, 8), dpi=150)

sns.lineplot(
    x="Game Prestige Score", 
    y="PK", 
    data=df_sorted,
    label="Pakistan (PK)", 
    linewidth=3
)

sns.lineplot(
    x="Game Prestige Score", 
    y="Group1", 
    data=df_sorted,
    label="Group1",
    linewidth=3
)

plt.title("Pakistan vs Group1 Performance Across Prestige Levels", fontsize=18)
plt.xlabel("Game Prestige Score", fontsize=14)
plt.ylabel("Medals Won", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

st.pyplot(fig3)












st.subheader("Regression Trend: Pakistan vs Other Countries")

with st.expander(" Select Country for Regression Plot"):
    reg_country = st.selectbox(
        "Choose a country:",
        ["IND", "IR", "CN", "UK", "GER", "AUS", "CAN", "USA"],
        index=0
    )

fig4 = plt.figure(figsize=(7, 5), dpi=130)

sns.regplot(
    x=df[reg_country],
    y=df["PK"],
    scatter_kws={'alpha': 0.5},
    line_kws={'color': 'red'}
)

plt.title(f"Pakistan vs {reg_country} — Regression Trend", fontsize=16)
plt.xlabel(reg_country, fontsize=13)
plt.ylabel("Pakistan (PK)", fontsize=13)
plt.grid(True, alpha=0.25)
plt.tight_layout()

st.pyplot(fig4)



st.subheader("Average Medals per Country (Across All Games)")

countries = ['PK', 'IND', 'IR', 'CN', 'UK', 'GER', 'AUS', 'CAN', 'USA']
avg_medals = df[countries].mean().sort_values()

fig5 = plt.figure(figsize=(12, 7), dpi=140)

sns.barplot(
    x=avg_medals.values,
    y=avg_medals.index,
    hue=avg_medals.index,
    dodge=False,
    palette="viridis",
    legend=False
)

plt.title("Average Medals per Country (Across 256 Games)", fontsize=18)
plt.xlabel("Average Medals", fontsize=14)
plt.ylabel("Country", fontsize=14)
plt.grid(True, axis="x", alpha=0.3)

st.pyplot(fig5)













st.subheader("Pakistan Medals vs Prestige Score (Negative Trend)")

fig6 = plt.figure(figsize=(10, 6), dpi=150)

sns.scatterplot(
    x="PK",
    y="Game Prestige Score",
    data=df,
    s=45,
    alpha=0.7
)

sns.regplot(
    x="PK",
    y="Game Prestige Score",
    data=df,
    scatter=False,
    ci=None,
    color='red'
)

plt.title("Pakistan Medals vs Prestige Score (Negative Trend)", fontsize=17)
plt.xlabel("Pakistan Medals (PK)", fontsize=14)
plt.ylabel("Game Prestige Score", fontsize=14)
plt.grid(True, alpha=0.3)

st.pyplot(fig6)
