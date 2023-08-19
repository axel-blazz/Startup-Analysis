import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Startup Funding Analysis")

df = pd.read_csv("startup_cleaned_2.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_investor_details(investor):
    st.title(investor)
    # Last 5 investments
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader("Last 5 investments")
    st.table(last5_df)

    col1, col2 = st.columns(2)

    
    with col1:    
        # Biggest investments
        st.subheader("Biggest Investments")
        biggest_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, axis = plt.subplots()
        axis.bar(biggest_df.index, biggest_df.values)
        st.pyplot(fig)
    
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader("Most Invested Verticals")
        fig, axis = plt.subplots()
        axis.pie(vertical_series.values, labels=vertical_series.index, autopct='%1.2f%%')
        st.pyplot(fig)

    col3, col4 = st.columns(2)
    with col3:
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader("Most Invested Rounds")
        fig, axis = plt.subplots()
        axis.pie(round_series.values, labels=round_series.index, autopct='%1.2f%%')
        st.pyplot(fig)
    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader("Most Invested Cities")
        fig, axis = plt.subplots()
        axis.pie(city_series.values, labels=city_series.index, autopct='%1.2f%%')
        st.pyplot(fig)

    st.subheader("Investments over the years")
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig, axis = plt.subplots()
    axis.plot(year_series.index, year_series.values)
    st.pyplot(fig)

    # Similar Investors
    st.subheader("Similar Investors")
    similar_investors = df[df['investors'].str.contains(investor)]['investors'].str.split(',').sum()
    similar_investors = pd.Series(similar_investors).value_counts().head(10)
    fig, axis = plt.subplots()
    axis.pie(similar_investors.values, labels=similar_investors.index)
    st.pyplot(fig)


def load_overall_details():
    # Total invested amount
    total = round(df['amount'].sum())
    # Max invested amount
    max_invested = df[df['amount'] == df['amount'].max()]
    # Average funding
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # Total funded startups
    total_funded = df['startup'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Invested Amount (in crores)", f"₹{total}")
    with col2:
        st.metric("Maximum Invested Amount (in crores)", f"₹{max_invested['amount'].values[0]}")
    with col3:
        st.metric("Average Funding (in crores)", f"₹{round(avg_funding)}")
    with col4:
        st.metric("Total Funded Startups", total_funded)
    
    st.header("Investments over the years")
    type = st.selectbox('Select Type', ['Amount', 'Startups'])
    if type == 'Amount':
        year_series = df.groupby('year')['amount'].sum()
        fig, axis = plt.subplots()
        axis.plot(year_series.index, year_series.values)
        st.pyplot(fig)
    else:
        year_series = df.groupby('year')['startup'].nunique()
        fig, axis = plt.subplots()
        axis.plot(year_series.index, year_series.values)
        st.pyplot(fig)


st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select a page", ["Overall Analysis", "Startup", "Investor"])

if option == "Overall Analysis":
    st.title("Overall Analysis")
    load_overall_details()
elif option == "Startup":
    st.title("Startup Analysis")
    selected_startup =st.sidebar.selectbox("Select a startup", sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find startup details")
elif option == "Investor":
    st.title("Investor Analysis")
    selected_investor = st.sidebar.selectbox("Select an investor", sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find investor details")

    if btn2:
        load_investor_details(selected_investor)
