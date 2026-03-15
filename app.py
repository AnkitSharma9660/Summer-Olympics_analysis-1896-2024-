import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Summer Olympics Analysis",
    page_icon="🏅",
    layout="wide"
)

# ---------- TITLE ----------
st.markdown(
    "<h1 style='text-align:center; color:#f9c74f;'>🏅 Summer Olympics Analysis Dashboard (1896–2024)</h1>",
    unsafe_allow_html=True
)

st.markdown("---")


# ---------- LOAD DATA ----------
import zipfile
with zipfile.ZipFile("olympics_dataset.zip") as z:
    df = pd.read_csv(z.open("olympics_dataset.csv"))
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

# ---------- SIDEBAR ----------
st.sidebar.title("Summer Olympics Analysis")
st.sidebar.image(
    "https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png",
    use_container_width=True
)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis')
)

# ---------- MEDAL TALLY ----------
if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")

    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally - {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} Overall Performance")
    else:
        st.title(f"{selected_country} Performance in {selected_year} Olympics")

    st.dataframe(medal_tally, use_container_width=True)

# ---------- OVERALL ANALYSIS ----------
if user_menu == 'Overall Analysis':

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", editions)
    col2.metric("Hosts", cities)
    col3.metric("Sports", sports)

    col1, col2, col3 = st.columns(3)
    col1.metric("Events", events)
    col2.metric("Nations", nations)
    col3.metric("Athletes", athletes)

    st.markdown("---")

    nations_over_time = helper.data_over_time(df, "region")
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.subheader("Participating Nations Over Years")
    st.plotly_chart(fig, use_container_width=True)

    events_over_time = helper.data_over_time(df, "Event")
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.subheader("Events Over Years")
    st.plotly_chart(fig, use_container_width=True)

    athletes_over_time = helper.data_over_time(df, "Name")
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.subheader("Athletes Over Years")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sport-wise Event Heatmap")

    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
        .fillna(0).astype(int),
        annot=True
    )
    st.pyplot(fig)

    st.subheader("Most Successful Athletes")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select Sport', sport_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)

# ---------- COUNTRY ANALYSIS ----------
if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)

    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f"{selected_country} Medal Tally Over Years")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"{selected_country} Performance in Sports")

    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.subheader(f"Top 10 Athletes of {selected_country}")

    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)
