import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Streamlit must be set first!
st.set_page_config(page_title="Provider Workload Dashboard", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    file_path = r"C:\Users\saich\Downloads\MRP_Dashboard\data\cleaned_data.csv"
    return pd.read_csv(file_path)

df = load_data()

# 🎨 Custom CSS for Styling
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        div[data-testid="metric-container"] {
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# 🚀 Title & Description
st.title("📊 Provider Workload Analysis Dashboard")
st.markdown("Analyze **Time in In Basket per Day** for **Internal Medicine providers** using live interactive charts.")

# 🔍 Sidebar Filters
st.sidebar.header("🔍 **Filter Data**")

service_area = st.sidebar.selectbox("📍 Select Service Area", ["All"] + list(df["ServiceArea"].unique()))
provider_type = st.sidebar.selectbox("🩺 Select Provider Type", ["All"] + list(df["ProviderType"].unique()))

# ✅ Apply filters dynamically
filtered_df = df.copy()
if service_area != "All":
    filtered_df = filtered_df[filtered_df["ServiceArea"] == service_area]
if provider_type != "All":
    filtered_df = filtered_df[filtered_df["ProviderType"] == provider_type]

# 📌 Key Metrics with Explanations
st.subheader("📌 **Key Metrics & Their Meaning**")

avg_time = filtered_df["Value"].mean()
total_providers = filtered_df["Provider Indentifier"].nunique()

col1, col2 = st.columns(2)
col1.metric("🕒 **Avg. Time in Basket (mins)**", f"{avg_time:.2f}")
col1.markdown("**📝 What it means:** The average time providers spend daily on administrative tasks.")

col2.metric("👨‍⚕️ **Total Providers Analyzed**", f"{total_providers}")
col2.markdown("**📊 Why it matters:** The number of unique providers included in the analysis.")

# 📈 Line Chart for Trends with Explanation
st.subheader("📈 **Time Trend Analysis**")
st.markdown("📌 **Insight:** This chart shows how **'Time in Basket Per Day'** changes over time, helping to identify trends in administrative workload.")

fig_time = px.line(filtered_df, x="ReportingPeriodStartDate", y="Value", color="ServiceArea",
                   title="Time in Basket Per Day Over Time", template="plotly_white")
st.plotly_chart(fig_time, use_container_width=True)

# 📊 Box Plot for Workload Distribution with Explanation
st.subheader("📊 **Provider Workload Distribution**")
st.markdown("📌 **Insight:** This boxplot compares the spread of administrative workload across different provider types.")

fig_box = px.box(filtered_df, x="ProviderType", y="Value", color="ProviderType",
                 title="Workload Distribution by Provider Type", template="plotly_white")
st.plotly_chart(fig_box, use_container_width=True)

# 🔥 Top 10 High-Workload Providers with Explanation
st.subheader("🔥 **Top 10 High-Workload Providers**")
st.markdown("📌 **Insight:** These are the top 10 providers spending the most time on administrative tasks.")

top_providers = filtered_df.groupby("Provider Indentifier")["Value"].mean().reset_index()
top_providers = top_providers.sort_values(by="Value", ascending=False).head(10)

fig_bar = px.bar(top_providers, x="Provider Indentifier", y="Value",
                 title="🏆 Top 10 Providers with Highest Time in Basket",
                 template="plotly_white", text_auto=True)
st.plotly_chart(fig_bar, use_container_width=True)

# 🎯 Insights & Actionable Steps
st.markdown("""
### 💡 **Key Takeaways**
✅ **Identify high-stress providers** and understand workload variations.  
✅ **Compare workloads across different service areas** to optimize staff allocation.  
✅ **Track trends over time** and identify operational bottlenecks.  

🚀 **Next Steps:** Use these insights to improve provider efficiency and reduce stress levels.
""")
