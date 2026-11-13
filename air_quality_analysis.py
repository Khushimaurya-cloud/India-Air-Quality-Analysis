import pandas as pd

df = pd.read_csv("air_quality_daily.csv")

df['date'] = pd.to_datetime(df['date']) #converting date column into datetime

print(df.dtypes)

print(df.head())

print(df.shape)

df.info()

print(df.describe())

print(df.isnull().sum())

print("Duplicate rows:", df.duplicated().sum())

print(df.dtypes)

df['year'] = df['date'].dt.year

yearly_aqi = df.groupby('year')['india_aqi'].mean()

print(yearly_aqi)

import matplotlib.pyplot as plt
yearly_aqi.plot(kind='bar')
plt.title('Year-wise Average AQI')
plt.xlabel('Year')
plt.ylabel('Average AQI')
plt.show()

#city-wise Average AQI

city_aqi = df.groupby('city')['india_aqi'].mean()
city_aqi = city_aqi.sort_values(ascending=False)
print("City-Wise Average AQI:")
print(city_aqi)

#Top 10 most polluted cities

top_10_cities = city_aqi.head(10)
top_10_cities.plot(kind='barh')
plt.title("Top 10 Most Polluted Cities")
plt.xlabel("Average AQI")
plt.ylabel("City")
plt.gca().invert_yaxis()
plt.show()

#Comparing Mumbai, Delhi and Pune
selected_cities = city_aqi.loc[['Mumbai', 'Delhi', 'Pune']]
print("Mumbai vs Delhi vs Pune:")
print(selected_cities)

# Mumbai vs Delhi vs Pune Graph
selected_cities.plot(kind='bar', color='skyblue')
plt.title('AQI Comparison: Mumbai vs Delhi vs Pune')
plt.xlabel('Cities')
plt.ylabel('Average AQI')
plt.show()

# Monthly Average AQI
monthly_aqi = df.groupby(
    df['date'].dt.to_period('M')
)['india_aqi'].mean()
print("Monthly Average AQI:")
print(monthly_aqi)

monthly_aqi.index = monthly_aqi.index.astype(str)
monthly_aqi.plot(kind='line', figsize=(12, 5))
plt.title('Monthly Average AQI Trend')
plt.xlabel('Month')
plt.ylabel('Average AQI')
plt.xticks(rotation=45)
plt.show()

# AQI Category Analysis
category_count = df['india_aqi_category'].value_counts()
print("AQI Category Distribution:")
print(category_count)

# PM2.5 vs PM10 Analysis
pm_comparison = df[['pm2_5_mean', 'pm10_mean']].mean()
print("PM2.5 vs PM10 Average:")
print(pm_comparison)

# PM2.5 vs PM10 Graph
pm_comparison.plot(kind='bar', color=['skyblue', 'orange'])
plt.title('PM2.5 vs PM10 Average Comparison')
plt.xlabel('Pollutants')
plt.ylabel('Average Level')
plt.show()