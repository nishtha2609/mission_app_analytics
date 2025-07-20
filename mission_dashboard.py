import streamlit as st
import pandas as pd
import altair as alt

# Load CSV
df = pd.read_csv("mission_internal_dashboard_data.csv", parse_dates=["Join Date"])
df["Month"] = df["Join Date"].dt.to_period("M").astype(str)

# Page config
st.set_page_config(page_title="Mission Internal Dashboard", layout="wide")
st.title("SRMD Mission App – Internal Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    region_filter = st.selectbox("Region", ["All"] + sorted(df["Region"].unique()))
    persona_filter = st.selectbox("Persona", ["All"] + sorted(df["Persona"].unique()))
    if region_filter != "All":
        df = df[df["Region"] == region_filter]
    if persona_filter != "All":
        df = df[df["Persona"] == persona_filter]

# Tab layout
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Management", "Content", "Design", "Tech", "Pre-Join", "Post-Launch"
])

# Management View
with tab1:
    st.header("Management View")
    col1, col2, col3 = st.columns(3)
    col1.metric("New Users Onboarded", len(df))
    col2.metric("Most Active Region", df["Region"].mode()[0])
    col3.metric("Most Common Funnel", df["User Funnel"].mode()[0])

    st.subheader("User Retention vs Churn")
    st.write("Cohort-wise Retention and Return Frequency")
    st.bar_chart(df[["Cohort Retention", "Return Frequency"]])

    st.subheader("Daily / Monthly Active Users")
    st.metric("Daily Active Users", df["Daily Active"].sum())
    st.metric("Monthly Active Users", df["Monthly Active"].sum())

    st.subheader("User Growth Over Time")
    st.line_chart(df.groupby("Month").size())

# Content View
with tab2:
    st.header("Content View")
    st.metric("Unique Viewers", df["Unique Viewer"].sum())
    st.metric("Viewers > 1 min", df["1+ Min Viewer"].sum())
    st.metric("Avg Completion Rate (%)", round(df["Content Completion Rate (%)"].mean(), 2))
    st.metric("Avg Total Watchtime (min)", round(df["Total Watchtime (min)"].mean(), 2))
    st.metric("Avg Depth Score", round(df["Content Depth Score"].mean(), 2))

    st.subheader("Most Watched Content")
    st.bar_chart(df["Most Watched Video"].value_counts())

# Design View
with tab3:
    st.header("Design View")
    st.metric("Avg Silent Scroll Rate", round(df["Silent Scroll Rate"].mean(), 2))
    st.metric("Avg Design Pause Time (s)", round(df["Design Pause Time (s)"].mean(), 2))
    st.metric("Avg Thumbnail CTR", round(df["Thumbnail CTR"].mean(), 2))

    st.subheader("Mood Drop-off")
    mood_df = df.groupby(["Mood Before", "Mood After"]).size().reset_index(name="Count")
    st.dataframe(mood_df)

# Tech View
with tab4:
    st.header("Tech Dashboard")
    st.metric("Avg Search Bar CTR", round(df["Search Bar CTR"].mean(), 2))
    st.metric("Avg App Load Time (ms)", round(df["App Load Time (ms)"].mean(), 1))
    st.metric("Avg Recommendation Accuracy", round(df["Recommendation Accuracy"].mean(), 2))
    st.metric("Avg App Downtime (hrs)", round(df["App Downtime (hrs)"].mean(), 2))
    st.metric("Avg Storage Used (GB)", round(df["Storage Used (GB)"].mean(), 2))

# Pre-Join View
with tab5:
    st.header("Pre-Joining Metrics")
    st.metric("Avg Onboarding Completion Rate", round(df["Onboarding Completion Rate"].mean(), 2))
    st.metric("Avg Mood Interaction Rate", round(df["Mood Interaction Rate"].mean(), 2))
    st.metric("Most Clicked Module", df["Top Clicked Module"].mode()[0])
    st.metric("Total Rewatches", df["Rewatches"].sum())
    st.metric("Total Skips", df["Skips"].sum())

# Post-Launch View
with tab6:
    st.header("Post-Launch Metrics")
    st.metric("Total Downloads", df["Total Downloads"].sum())
    st.metric("Total Deletions", df["Total Deletions"].sum())
    st.metric("Total Support Requests", df["Support Requests"].sum())
    st.metric("Avg Return Frequency", round(df["Return Frequency"].mean(), 2))
    st.metric("Avg Cohort Retention", round(df["Cohort Retention"].mean(), 2))
