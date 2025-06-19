import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Load the updated CSV
df = pd.read_csv("C:/Users/bkdee/Downloads/energy_consumption.csv")

# Parse datetime and extract components
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%d-%m-%Y %H:%M')
df['Hour'] = df['Datetime'].dt.hour
df['Day'] = df['Datetime'].dt.date
df['Week_Start'] = df['Datetime'].dt.to_period('W').apply(lambda r: r.start_time)
df['Date'] = df['Datetime'].dt.date

# Rename PJME_MW column if necessary
if 'PJME_MW' in df.columns:
    df.rename(columns={'PJME_MW': 'Load'}, inplace=True)
# Adjust load values based on Device_Type and Location (realistic simulation)
adjustment_factors = {
    'Home': {
        'AC': 0.6,
        'Refrigerator': 1.0,
        'Lights': 1.2,
        'TV': 1.1
    },
    'Company': {
        'AC': 1.6,
        'Refrigerator': 0.8,
        'Lights': 1.4,
        'TV': 0.7
    }
}

# Apply adjusted load
df['Adjusted_Load'] = df.apply(
    lambda row: row['Load'] * adjustment_factors[row['Location']][row['Device_Type']],
    axis=1
)
# Extract year from datetime
df['Year'] = df['Datetime'].dt.year

# Group by Year and Region, aggregate Adjusted_Load
yearly_region_load = df.groupby(['Year', 'Region'])['Adjusted_Load'].mean().reset_index()


# --- SQL Analysis in Memory ---
conn = sqlite3.connect(":memory:")
df.to_sql("energy", conn, index=False, if_exists="replace")

# Peak Load by Hour
peak_usage = pd.read_sql_query("""
SELECT Hour, MAX(Load) as Peak_Load
FROM (SELECT strftime('%H', Datetime) as Hour, Load FROM energy)
GROUP BY Hour
ORDER BY Hour
""", conn)

# --- Visualizations ---

# 1. Average Weekly Load
weekly_avg = df.groupby('Week_Start')['Load'].mean().reset_index().rename(columns={'Load': 'Avg_Weekly_Load'})

plt.figure(figsize=(12,6))
plt.plot(weekly_avg['Week_Start'], weekly_avg['Avg_Weekly_Load'], marker='o', linestyle='-')
plt.title("Average Weekly Load")
plt.xlabel("Week Start Date")
plt.ylabel("Load (MW)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. Average Daily Load
avg_daily = df.groupby('Day')['Load'].mean().reset_index().rename(columns={'Load': 'Avg_Daily_Load'})
plt.figure(figsize=(12,6))
plt.plot(avg_daily['Day'], avg_daily['Avg_Daily_Load'], color='teal')
plt.title("Average Daily Load")
plt.xlabel("Date")
plt.ylabel("Load (MW)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Peak Usage Time by Hour
plt.figure(figsize=(10,5))
sns.barplot(data=peak_usage, x='Hour', y='Peak_Load', palette='rocket')
plt.title("Peak Usage by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Peak Load (MW)")
plt.tight_layout()
plt.show()

# 4. Heatmap: Load by Hour and Date
pivot = df.pivot_table(index='Hour', columns='Date', values='Load')
plt.figure(figsize=(14, 6))
sns.heatmap(pivot, cmap='YlOrRd')
plt.title("Heatmap of Energy Load by Hour and Date")
plt.xlabel("Date")
plt.ylabel("Hour")
plt.tight_layout()
plt.show()

# 5. Energy Usage Over Time by Region
# Convert Datetime to Week Start
plt.figure(figsize=(14, 6))
sns.lineplot(data=yearly_region_load, x='Year', y='Adjusted_Load', hue='Region', marker='o', palette='tab10')
plt.title("Average Energy Load Over Years by Region")
plt.xlabel("Year")
plt.ylabel("Average Adjusted Load (MW)")
plt.grid(True)
plt.xticks(sorted(df['Year'].unique()), rotation=45)
plt.legend(title="Region")
plt.tight_layout()
plt.show()


# 6. Average Load by Device Type and Location (Home vs Company)
device_location_avg = df.groupby(['Device_Type', 'Location'])['Adjusted_Load'].mean().reset_index()

plt.figure(figsize=(12,6))
sns.barplot(data=device_location_avg, x='Device_Type', y='Adjusted_Load', hue='Location', palette='Set2')
plt.title("Realistic Average Load by Device Type: Home vs Company")
plt.xlabel("Device Type")
plt.ylabel("Adjusted Load (MW)")
plt.legend(title="Location")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



