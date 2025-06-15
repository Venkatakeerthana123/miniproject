import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df = pd.read_csv("C:/Users/bkdee/Downloads/energy.csv")  # Replace with actual filename
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d-%m-%Y %H:%M')
df['Hour'] = df['Datetime'].dt.hour
df['Day'] = df['Datetime'].dt.date

# Rename PJME_MW column
df.rename(columns={'PJME_MW': 'Load'}, inplace=True)

# --- SQL Implementation using SQLite in-memory ---
conn = sqlite3.connect(":memory:")
df.to_sql("energy", conn, index=False, if_exists="replace")

# 1. Peak Usage Time (Max Load per Hour)
peak_usage = pd.read_sql_query("""
SELECT Hour, MAX(Load) as Peak_Load
FROM (SELECT strftime('%H', Datetime) as Hour, Load FROM energy)
GROUP BY Hour
ORDER BY Hour
""", conn)

# 2. Average Daily Load
avg_daily = pd.read_sql_query("""
SELECT Day, AVG(Load) as Avg_Daily_Load
FROM (SELECT DATE(Datetime) as Day, Load FROM energy)
GROUP BY Day
ORDER BY Day
""", conn)

# --- Python Visualizations ---

# Plot 1: Average Daily Load
plt.figure(figsize=(12,6))
plt.plot(avg_daily['Day'], avg_daily['Avg_Daily_Load'])
plt.title("Average Daily Load")
plt.xlabel("Date")
plt.ylabel("Load (MW)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Peak Usage Time (Hourly)
plt.figure(figsize=(10,5))
sns.barplot(data=peak_usage, x='Hour', y='Peak_Load', palette='viridis')
plt.title("Peak Usage by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Peak Load (MW)")
plt.show()

# Optional Heatmap: Load by Hour and Date
df['Date'] = df['Datetime'].dt.date
df['Hour'] = df['Datetime'].dt.hour
pivot = df.pivot_table(index='Hour', columns='Date', values='Load')

plt.figure(figsize=(14, 6))
sns.heatmap(pivot, cmap='YlOrRd')
plt.title("Heatmap of Energy Load by Hour and Date")
plt.xlabel("Date")
plt.ylabel("Hour")
plt.tight_layout()
plt.show()