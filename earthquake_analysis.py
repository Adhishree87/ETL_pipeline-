import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🔹 Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",  
    password="postgres"  
)

#  Fetch Data from PostgreSQL
query = "SELECT * FROM earthquake_data;"
df = pd.read_sql(query, conn)

#  Close connection
conn.close()
print("Total number of earthquakes:", len(df))


#  Ensure 'time' column is in datetime format
df['time'] = pd.to_datetime(df['time'])

### Basic Summary Statistics**
print("Summary Statistics:")
print(df.describe())

### Magnitude Distribution Analysis
plt.figure(figsize=(10,6))
sns.histplot(df['magnitude'], bins=30, kde=True, color='blue')
plt.title('Earthquake Magnitude Distribution')
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.show()

###Depth vs. Magnitude Analysis**
plt.figure(figsize=(10,6))
sns.scatterplot(x=df['depth'], y=df['magnitude'], alpha=0.6)
plt.title('Depth vs Magnitude')
plt.xlabel('Depth (km)')
plt.ylabel('Magnitude')
plt.show()

###  Earthquake Frequency Over Time**
df.set_index('time', inplace=True)  # Set 'time' as index
df.resample('M').size().plot(figsize=(12,6), marker='o', linestyle='-')
plt.title('Monthly Earthquake Frequency')
plt.xlabel('Time')
plt.ylabel('Number of Earthquakes')
plt.show()

### Most Affected Locations**
plt.figure(figsize=(12,6))
df['place'].value_counts().head(10).plot(kind='bar', color='red')
plt.title('Top 10 Most Affected Locations')
plt.xlabel('Location')
plt.ylabel('Number of Earthquakes')
plt.xticks(rotation=45)
plt.show()

### Mapping Earthquakes (Longitude vs. Latitude)**
plt.figure(figsize=(12,6))
sns.scatterplot(x=df['longitude'], y=df['latitude'], hue=df['magnitude'], palette='coolwarm', size=df['magnitude'])
plt.title('Geographical Distribution of Earthquakes')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

### Correlation Analysis**
plt.figure(figsize=(8,6))
sns.heatmap(df[['magnitude', 'depth', 'longitude', 'latitude']].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()
