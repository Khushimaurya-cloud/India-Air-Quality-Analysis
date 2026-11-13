
import streamlit as st
import pandas as pd

st.set_page_config(page_title="India Air Quality Dashboard", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #F5F0FA !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #F5F0FA !important;
}

h1, h2, h3 {
    color: purple !important;
}

p, label {
    color: #333333 !important;
}

[data-testid="stSidebar"] {
    background-color: #EDE5F5 !important;
}

[data-testid="stMetric"] {
    background-color: white !important;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #DDDDDD;
}

[data-testid="stMetricValue"] {
    color: purple !important;
}
</style>
""", unsafe_allow_html=True)

st.title("India Air Quality Analysis Dashboard")

df = pd.read_csv("air_quality_daily.csv")
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

st.sidebar.header("Filters")

years = sorted(df['year'].unique())
cities = sorted(df['city'].dropna().unique())

st.sidebar.write("Total Cities:", len(cities))

year = st.sidebar.selectbox("Select Year", ["All Years"] + years)
city = st.sidebar.selectbox("Select City", ["All Cities"] + cities)

filtered_df = df.copy()

if year != "All Years":
    filtered_df = filtered_df[filtered_df['year'] == year]

if city != "All Cities":
    filtered_df = filtered_df[filtered_df['city'] == city]

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))
col2.metric("Average AQI", round(filtered_df['india_aqi'].mean(), 2))
col3.metric("Total Cities", filtered_df['city'].nunique())

st.subheader("Dataset Overview")

columns = [
    'date', 'city', 'india_aqi', 'india_aqi_category',
    'dominant_pollutant', 'pm2_5_mean', 'pm10_mean',
    'no2_mean', 'so2_mean'
]

st.dataframe(filtered_df[columns], use_container_width=True)

st.subheader("1. Year-wise Average AQI")
st.bar_chart(filtered_df.groupby('year')['india_aqi'].mean())

st.subheader("2. Top 10 Most Polluted Cities")
city_aqi = filtered_df.groupby('city')['india_aqi'].mean()
st.bar_chart(city_aqi.sort_values(ascending=False).head(10))

st.subheader("3. AQI Category Distribution")
st.bar_chart(filtered_df['india_aqi_category'].value_counts())

st.subheader("4. Monthly AQI Trend")

monthly = filtered_df.groupby(
    filtered_df['date'].dt.to_period('M')
)['india_aqi'].mean()

monthly.index = monthly.index.astype(str)
st.line_chart(monthly)

st.subheader("5. PM2.5 vs PM10")
pm = filtered_df[['pm2_5_mean', 'pm10_mean']].mean()
st.bar_chart(pm)

st.subheader("6. Mumbai vs Delhi vs Pune")

comparison = filtered_df[
    filtered_df['city'].isin(['Mumbai', 'Delhi', 'Pune'])
].groupby('city')['india_aqi'].mean()

st.bar_chart(comparison)
