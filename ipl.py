
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your datasets
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

sns.set_theme(style="whitegrid")

# Create a dashboard with six plots
fig, axes = plt.subplots(3, 2, figsize=(16, 18))

# 1. Matches played in each season
season_counts = matches.groupby("season")["id"].count()

season_counts.plot(
    kind="bar", ax=axes[0, 0]
)
axes[0, 0].set_title("IPL Matches Per Season")
axes[0, 0].set_xlabel("Season")
axes[0, 0].set_ylabel("Matches")
axes[0, 0].tick_params(axis="x", rotation=45)

# 2. Total matches won by each team
team_wins = matches["winner"].value_counts().head(10)

team_wins.sort_values().plot(
    kind="barh", ax=axes[0, 1]
)
axes[0, 1].set_title("Top 10 Teams by Match Wins")
axes[0, 1].set_xlabel("Matches Won")

# 3. Top 10 run scorers
top_batters = (
    deliveries.groupby("batter")["batsman_runs"]
    .sum()
    .nlargest(10)
    .sort_values()
)

top_batters.plot(
    kind="barh", ax=axes[1, 0]
)
axes[1, 0].set_title("Top 10 Run Scorers")
axes[1, 0].set_xlabel("Total Runs")

# 4. Top 10 wicket takers
valid_wickets = deliveries[
    deliveries["is_wicket"].eq(1)
    & ~deliveries["dismissal_kind"].isin(
        ["run out", "retired hurt", "obstructing the field",
         "retired out"]
    )
]

top_bowlers = (
    valid_wickets.groupby("bowler")
    .size()
    .nlargest(10)
    .sort_values()
)

top_bowlers.plot(
    kind="barh", ax=axes[1, 1]
)
axes[1, 1].set_title("Top 10 Wicket Takers")
axes[1, 1].set_xlabel("Wickets")

# 5. Toss decisions
matches["toss_decision"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=axes[2, 0]
)
axes[2, 0].set_title("Toss Decision Distribution")
axes[2, 0].set_ylabel("")

# 6. Total runs scored by batting team
team_runs = (
    deliveries.groupby("batting_team")["total_runs"]
    .sum()
    .nlargest(10)
    .sort_values()
)

team_runs.plot(
    kind="line", ax=axes[2, 1]
)
axes[2, 1].set_title("Top 10 Teams by Total Runs")
axes[2, 1].set_xlabel("Total Runs")

plt.tight_layout()

# Save the dashboard as an image
plt.savefig("ipl_analysis_plots.png", dpi=300, bbox_inches="tight")

# Display all six plots
plt.show()

print("IPL plotting completed!")
print("Dashboard saved as ipl_analysis_plots.png")