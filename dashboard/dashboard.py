import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
sns.set_context("notebook", font_scale=1.2)

#Siapkan seluruh DataFrame untuk visualisasi

#Fungsi untuk membuat DataFrame sum order items
def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english")["product_id"].count().reset_index()
    sum_order_items_df.rename(columns={
        "product_id": "products",
        "product_category_name_english":"category"
    }, inplace=True)
    sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)

    return sum_order_items_df
#Fungsi untuk membuat DataFrame dengan mengelompokkan berdasarkan state/negara bagian
def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id_customers.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id_customers": "customer_count"
    }, inplace=True)

    return bystate_df
#Fungsi untuk membuat DataFrame dengan mengelompokkan berdasarkan city/kota
def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id_customers.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id_customers": "customer_count"
    }, inplace=True)

    return bycity_df
#Fungsi untuk membuat DataFrame berdasarkan payment type 
def create_payment_counts(df):
    payment_counts = df['payment_type'].value_counts().reset_index()
    payment_counts.columns = ['payment_type', 'count']

    return payment_counts
#Fungsi untuk membuat DataFrame rating summary
def create_rating_summary(df):
    rating_summary = df['review_score'].value_counts().sort_index()

    return rating_summary

#Load file all data
all_df = pd.read_csv("all_data.csv")

#Memanggil helper function yang telah dibuat
sum_order_items_df = create_sum_order_items_df(all_df)
bystate_df = create_bystate_df(all_df)
bycity_df = create_bycity_df(all_df)
payment_counts = create_payment_counts(all_df)
rating_summary = create_rating_summary(all_df)

#Menambahkan header pada dashboard tersebut
st.header('E-commerce Public Dashboard :sparkles:')

#Membuat visualisasi untuk produk yang paling banyak dan paling sedikit terjual
st.subheader("Best-Selling and Least-Selling Product")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
colors_best = ["#00FF57", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_least = ["#F90611", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="products", y="category", data=sum_order_items_df.sort_values(by="products", ascending=False).head(5), palette=colors_best, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best-Selling Products", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)

sns.barplot(x="products", y="category", data=sum_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors_least, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least-Selling Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

#Membuat visualisasi lokasi geografis customer
st.subheader("Customer Geographic Location")
#untuk bystate
fig, ax=plt.subplots(figsize=(16, 8))
colors1= ["#8EACCD", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3"]
sns.barplot(x="customer_count", y="customer_state", data=bystate_df.sort_values(by="customer_count", ascending=False).head(10), palette=colors1, ax=ax)
ax.set_title("Number of Customers by States", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)
#untuk bycity
fig, ax=plt.subplots(figsize=(16, 8))
colors1= ["#6A9C89", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3"]
sns.barplot(x="customer_count", y="customer_city", data=bycity_df.sort_values(by="customer_count", ascending=False).head(10), palette=colors1, ax=ax)
ax.set_title("Number of Customers by City", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#Membuat visualisasi payment type yang paling banyak digunakan
st.subheader("Payment Types")
fig, ax = plt.subplots(figsize=(16,8))
colors2= ["#16423C", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3"]
top_payment_types = payment_counts.sort_values(by='count', ascending=False)
sns.barplot(x='payment_type', y='count', data=top_payment_types, palette=colors2, ax=ax)
ax.set_title('Most Used Payment Types by Customers', loc="center", fontsize=15)
ax.set_xlabel('Number of Transactions', fontsize=15)
ax.set_ylabel('Payment Type', fontsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=15)
plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.9)
st.pyplot(fig)

#Membuat visualisasi rating summary yang diberikan oleh customer
st.subheader("Rating Summary")
fig, ax = plt.subplots(figsize=(16,8))
colors3= ["#B8001F", "#D3D3D3", "#D3D3D3", "#D3D3D3","#347928"]
sns.countplot(x='review_score', data=all_df, palette=colors3, ax=ax)
ax.set_title('Customer Satisfaction Review', loc="center", fontsize=30)
ax.set_xlabel('Satisfaction Rating (1 to 5)', fontsize=20)
ax.set_ylabel('Number of Customers', fontsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
plt.subplots_adjust(bottom=0.15, top=0.9, left=0.1, right=0.9)
st.pyplot(fig)

#Menambahkan copyright
st.caption('Copyright (c) Grace Loisa 2024')
