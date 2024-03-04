import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")


day_df.drop_duplicates(inplace=True)
hour_df.drop_duplicates(inplace=True)


all_df = pd.merge(left=day_df, right=hour_df, how="left", left_on="instant", right_on="instant")


all_df['dteday_x'] = pd.to_datetime(all_df['dteday_x'])
all_df.set_index('dteday_x', inplace=True)


all_df_2012 = all_df[all_df.index.year == 2012]
monthly_orders_df = all_df_2012.resample(rule='M').agg({
    "instant": "nunique",
})

monthly_orders_df.rename(columns={
    "instant": "order_count"
}, inplace=True)
monthly_orders_df.index = monthly_orders_df.index.strftime('%B %Y')

st.write("## Number of Orders per Month (2012)")
st.table(monthly_orders_df)
st.line_chart(monthly_orders_df['order_count'])


season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
all_df['season'] = all_df['season_x'].map(season_mapping)
season_orders = all_df.groupby('season').size().reset_index(name='order_count')
season_bar_orders = all_df.groupby('season').size()
st.write("## Number of Orders by Season")
st.table(season_orders)
st.bar_chart(season_bar_orders)