import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df = pd.read_csv("C:/Users/bkdee/Downloads/energy.csv")  # Replace with actual filename
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d-%m-%Y %H:%M')
df['Hour'] = df['Datetime'].dt.hour
df['Day'] = df['Datetime'].dt.date
device_types = ['AC', 'Heater', 'Fridge', 'TV', 'Washer']
df['Device_Type'] = [device_types[i % len(device_types)] for i in range(len(df))]
regions = ['North', 'South', 'East', 'West', 'Central']
df['Region'] = [regions[i % len(regions)] for i in range(len(df))]


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
# Calculate Average Weekly Load
df['Week_Start'] = df['Datetime'].dt.to_period('W').apply(lambda r: r.start_time)
weekly_avg = df.groupby('Week_Start')['Load'].mean().reset_index().rename(columns={'Load': 'Avg_Weekly_Load'})

plt.figure(figsize=(12,6))
plt.plot(weekly_avg['Week_Start'], weekly_avg['Avg_Weekly_Load'], marker='o', linestyle='-')
plt.title("Average Weekly Load")
plt.xlabel("Week Start Date")
plt.ylabel("Load (MW)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
# --- Python Visualizations ---

# Plot 1: Average Daily Load
avg_daily = df.groupby('Day')['Load'].mean().reset_index().rename(columns={'Load': 'Avg_Daily_Load'})
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
sns.barplot(data=peak_usage, x='Hour', y='Peak_Load')
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

# Plot 3: Average Load by Device Type
device_avg = df.groupby('Device_Type')['Load'].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(data=device_avg, x='Device_Type', y='Load', palette='mako')
plt.title("Average Load by Device Type")
plt.xlabel("Device Type")
plt.ylabel("Average Load (MW)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 4: Energy Usage Over Time by Region
region_time = df.groupby(['Datetime', 'Region'])['Load'].sum().reset_index()
plt.figure(figsize=(14, 6))
sns.lineplot(data=region_time, x='Datetime', y='Load', hue='Region', palette='tab10')
plt.title("Energy Usage Over Time by Region")
plt.xlabel("Time")
plt.ylabel("Load (MW)")
plt.xticks(rotation=45)
plt.legend(title="Region")
plt.tight_layout()
plt.show()