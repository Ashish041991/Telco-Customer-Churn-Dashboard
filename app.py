import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Dashboard Layout Settings
st.set_page_config(page_title="Telco Churn Dashboard", layout="wide")
st.title("📊 Subscriber Retention & Customer Churn Analytics")

# 2. Optimized Data Loading Pipeline
csv_filename = "Telco-Customer-Churn.csv"

@st.cache_data
def load_churn_data():
    df = pd.read_csv(csv_filename)
    # Convert empty space anomalies in TotalCharges to numeric values
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].str.strip(), errors='coerce').fillna(0)
    return df

try:
    df = load_churn_data()
    
    # 3. Sidebar Filter Widget Configuration
    st.sidebar.header("🎯 Dashboard Filter Options")

    # Get unique values for internet services to populate our dropdown
    internet_options = ["All"] + list(df['InternetService'].unique())
    selected_internet = st.sidebar.selectbox("Filter by Internet Service Type:", internet_options)

    # Apply the filter selection dynamically to the dataframe
    if selected_internet != "All":
        filtered_df = df[df['InternetService'] == selected_internet]
    else:
        filtered_df = df
    
    # 4. High-Level Executive Metric Cards (Using filtered data variables)
    st.subheader("📋 Executive Summary Insights")
    col1, col2, col3 = st.columns(3)
    
    total_cust_f = filtered_df.shape[0]
    churn_count_f = filtered_df[filtered_df['Churn'] == 'Yes'].shape[0]
    churn_rate_f = round((churn_count_f / total_cust_f) * 100, 2) if total_cust_f > 0 else 0
    avg_tenure_f = round(filtered_df['tenure'].mean(), 1) if total_cust_f > 0 else 0
    
    col1.metric("Total Subscribers", f"{total_cust_f:,}")
    col2.metric("Overall Churn Rate", f"{churn_rate_f}%", delta=f"{churn_count_f} Losses", delta_color="inverse")
    col3.metric("Avg. Account Lifespan", f"{avg_tenure_f} Mos")

    # 5. Interactive Plotly Graph using filtered_df
    st.subheader("📈 Risk Assessment Factor Matrices")
    
    fig_contract = px.histogram(
        filtered_df, 
        x="Contract", 
        color="Churn", 
        barmode="group",
        title=f"Attrition Density by Contract Type ({selected_internet} Services)",
        color_discrete_sequence=["#2ECC71", "#E74C3C"], # Green vs Red
        labels={"Contract": "Subscription Contract Model", "count": "Subscriber Base Count"}
    )
    st.plotly_chart(fig_contract, use_container_width=True)

    # 6. Data Frame Explorer
    st.subheader("🔍 Raw Data Sub-Matrix Explorer")
    st.dataframe(filtered_df.head(100), use_container_width=True)

except FileNotFoundError:
    st.error(f"❌ File '{csv_filename}' not detected. Ensure it is placed directly inside your project folder.")