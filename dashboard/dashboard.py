import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

def get_total_count_by_hourly_data(hourly_data):
  hourly_rentals_count =  hourly_data.groupby(by="hour").agg({"cnt": ["sum"]})
  return hourly_rentals_count

def count_by_daily_data(daily_data):
    daily_rentals_2011 = daily_data.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    return daily_rentals_2011

def total_registered_df(daily_data):
   daily_registered_rentals =  daily_data.groupby(by="date").agg({
      "registered": "sum"
    })
   daily_registered_rentals = daily_registered_rentals.reset_index()
   daily_registered_rentals.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return daily_registered_rentals

def total_casual_df(daily_data):
   daily_casual_rentals =  daily_data.groupby(by="date").agg({
      "casual": ["sum"]
    })
   daily_casual_rentals = daily_casual_rentals.reset_index()
   daily_casual_rentals.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return daily_casual_rentals

def sum_order (hourly_data):
    hourly_total_rentals = hourly_data.groupby("hour").cnt.sum().sort_values(ascending=False).reset_index()
    return hourly_total_rentals

def another_season (daily_data): 
    seasonal_rentals = daily_data.groupby(by="season").cnt.sum().reset_index() 
    return seasonal_rentals

file_path_daily = './cleaned_day_data.csv'
file_path_hourly = './cleaned_hour_data.csv'

daily_data = pd.read_csv(file_path_daily)
hourly_data = pd.read_csv(file_path_hourly)


datetime_columns = ["date"]
daily_data.sort_values(by="date", inplace=True)
daily_data.reset_index(inplace=True)   

hourly_data.sort_values(by="date", inplace=True)
hourly_data.reset_index(inplace=True)

for column in datetime_columns:
    daily_data[column] = pd.to_datetime(daily_data[column])
    hourly_data[column] = pd.to_datetime(hourly_data[column])

min_date_daily_data = daily_data["date"].min()
max_date_daily_data = daily_data["date"].max()

min_date_hourly_data = hourly_data["date"].min()
max_date_hourly_data = hourly_data["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("../bike.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_daily_data,
        max_value=max_date_daily_data,
        value=[min_date_daily_data, max_date_daily_data])
  
main_df_days = daily_data[(daily_data["date"] >= str(start_date)) & 
                        (daily_data["date"] <= str(end_date))]

main_df_hour = hourly_data[(hourly_data["date"] >= str(start_date)) & 
                        (hourly_data["date"] <= str(end_date))]

hourly_rentals_count = get_total_count_by_hourly_data(main_df_hour)
daily_rentals_2011 = count_by_daily_data(main_df_days)
daily_registered_rentals = total_registered_df(main_df_days)
daily_casual_rentals = total_casual_df(main_df_days)
hourly_total_rentals = sum_order(main_df_hour)
seasonal_rentals = another_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Dat
st.header('Bike Sharing Analysis :rocket:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = daily_rentals_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = daily_registered_rentals.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = daily_casual_rentals.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Pada jam berapa jumlah penyewaan sepeda tertinggi dan terendah dalam satu hari?")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='hour', y='cnt', data=hourly_data, ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)


st.subheader("Seberapa besar pengaruh cuaca terhadap jumlah penyewaan sepeda?")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='weather_situation', y='cnt', data=hourly_data, ax=ax)
ax.set_title('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)
 
st.subheader("Apakah hari kerja memiliki jumlah penyewaan yang lebih tinggi dibandingkan akhir pekan atau hari libur?")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='workingday', y='cnt', data=daily_data, ax=ax)
ax.set_title('Pengaruh Hari Kerja terhadap Jumlah Penyewaan Sepeda')
ax.set_xlabel('Hari Kerja (0: Bukan Hari Kerja, 1: Hari Kerja)')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

st.subheader("Bagaimana tren penggunaan sepeda berubah antara tahun 2011 dan 2012?")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='month', y='cnt', hue='year', data=daily_data, ax=ax)
ax.set_title('Tren Penggunaan Sepeda per Bulan (2011 vs 2012)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)
