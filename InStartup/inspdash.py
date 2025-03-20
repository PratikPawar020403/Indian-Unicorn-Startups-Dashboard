import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set page configuration for modern UI
st.set_page_config(
    page_title="Indian Unicorn Startups Dashboard", page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
def load_data():
    data = pd.read_csv("InStartup/Indian Unicorn startups 2023 updated.csv")
    data = data.rename(columns={
        'Entry Valuation^^ ($B)': 'Entry Valuation ($B)',
        'Valuation ($B)': 'Current Valuation ($B)'
    })
    data['Year'] = pd.to_datetime(data['Entry'], errors='coerce').dt.year
    return data

data = load_data()

# Custom CSS for a dark and clean UI
st.markdown("""
    <style>
    /* General dark theme styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #121212;  /* Dark background for sleekness */
        color: #FFFFFF;  /* White text for contrast */
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #1C1C1C;
        color: #FFFFFF;
    }

    /* Header Styling */
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        font-weight: 700;  /* Bold for headings */
        color: #FF5733;
    }

    /* KPI Card Styling */
    .kpi-card {
        background-color: #2E2E2E;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        height: 180px;  /* Medium, clean size for key metrics */
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        flex-direction: column;
        transition: all 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);
    }

    .kpi-card h3 {
        font-size: 1.6em;
        color: #FF5733;
        margin-bottom: 10px;
    }

    .kpi-card p {
        font-size: 1.2em;
        color: #DDDDDD;
    }

    /* Section title styling */
    .section-title {
        font-size: 2.4em;
        font-weight: 700;
        color: #FF5733;
        margin-top: 30px;
    }

    /* WordCloud styling */
    .wordcloud-container {
        background-color: #2E2E2E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

 /* Footer Styling with bold and dark colors */
    .footer {
        text-align: center;
        padding: 20px 0;
        font-size: 1.1em;
        color: #FF5733;  /* White color for footer text */

        font-weight: bold;  /* Bold font */
        border-top: 2px solid #FF5733;  /* Orange border for emphasis */
    }

    .footer a {
        color: #FF5733;  /* Orange link color */
        text-decoration: none;
            
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.title("Filters")
sector_filter = st.sidebar.multiselect("Select Sector", options=data["Sector"].unique(), default=[])
year_filter = st.sidebar.slider("Select Year", int(data["Year"].min()), int(data["Year"].max()), (int(data["Year"].min()), int(data["Year"].max())))
location_filter = st.sidebar.multiselect("Select Location", options=data["Location"].unique(), default=[])

# Apply filters
filtered_data = data[
    (data["Sector"].isin(sector_filter) if sector_filter else True) &
    (data["Year"].between(*year_filter)) &
    (data["Location"].isin(location_filter) if location_filter else True)
]

# Header
st.title("🦄 Indian Unicorn Startups Dashboard")
st.markdown("Explore the trends, funding, and insights into Indian Unicorns of 2023.")

# KPI Section (Key Metrics)
st.markdown("### 📊 Key Metrics")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown("""
        <div class="kpi-card">
            <h3>Total Unicorns</h3>
            <p>{}</p>
        </div>
    """.format(len(filtered_data)), unsafe_allow_html=True)

with kpi_col2:
    st.markdown("""
        <div class="kpi-card">
            <h3>Total Valuation ($B)</h3>
            <p>{}</p>
        </div>
    """.format(round(filtered_data["Current Valuation ($B)"].sum(), 2)), unsafe_allow_html=True)

with kpi_col3:
    st.markdown("""
        <div class="kpi-card">
            <h3>Average Entry Valuation ($B)</h3>
            <p>{}</p>
        </div>
    """.format(round(filtered_data["Entry Valuation ($B)"].mean(), 2)), unsafe_allow_html=True)

with kpi_col4:
    # Median Valuation ($B) for Key Metrics
    median_valuation = filtered_data["Current Valuation ($B)"].median()
    st.markdown("""
        <div class="kpi-card">
            <h3>Median Valuation ($B)</h3>
            <p>{}</p>
        </div>
    """.format(round(median_valuation, 2)), unsafe_allow_html=True)

# 🌍 Geographical Insights Section
st.markdown("### 🌍 Geographical Insights")
geo_col1, geo_col2 = st.columns(2)

# Top Locations by Unicorn Count
with geo_col1:
    top_locations = filtered_data['Location'].value_counts().head(10).reset_index()
    top_locations.columns = ['Location', 'Count']
    location_chart = px.bar(top_locations, x='Location', y='Count', color='Location', title='Top Locations by Unicorn Count', color_continuous_scale='Viridis')
    st.plotly_chart(location_chart, use_container_width=True)

# Total Valuation by Location
with geo_col2:
    total_valuation_by_location = filtered_data.groupby('Location')['Current Valuation ($B)'].sum().reset_index()
    total_valuation_by_location = total_valuation_by_location.sort_values('Current Valuation ($B)', ascending=False).head(10)
    valuation_chart = px.bar(total_valuation_by_location, x='Location', y='Current Valuation ($B)', color='Location', title='Total Valuation by Location', color_continuous_scale='Viridis')
    st.plotly_chart(valuation_chart, use_container_width=True)

# 📂 Sector Insights Section
st.markdown("### 📂 Sector Insights")
sector_col1, sector_col2 = st.columns(2)

# Top Sectors by Unicorn Count
with sector_col1:
    top_sectors = filtered_data['Sector'].value_counts().head(10).reset_index()
    top_sectors.columns = ['Sector', 'Count']
    sector_chart = px.bar(top_sectors, x='Sector', y='Count', color='Sector', title='Top Sectors by Unicorn Count', color_continuous_scale='YlOrRd')
    st.plotly_chart(sector_chart, use_container_width=True)

# Sector Distribution (Pie chart, default 5 sectors)
with sector_col2:
    sector_dist = filtered_data['Sector'].value_counts().head(5).reset_index()
    sector_dist.columns = ['Sector', 'Count']
    sector_pie_chart = px.pie(sector_dist, values='Count', names='Sector', title='Sector Distribution', color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(sector_pie_chart, use_container_width=True)

# 📅 Yearly Line Chart
st.markdown("### 📅 Yearly Unicorn Growth Trend")
yearly_data = filtered_data.groupby("Year").size().reset_index(name="Unicorn Count")
yearly_line_chart = px.line(yearly_data, x="Year", y="Unicorn Count", title="Yearly Unicorn Growth", markers=True)
st.plotly_chart(yearly_line_chart, use_container_width=True)

# Word Cloud for Investors
st.header("🤝 Key Investors")
st.subheader("Top Investors Word Cloud")

investors = ' '.join(filtered_data['Select Investors'].dropna())
wordcloud = WordCloud(background_color='white', colormap='tab10', width=800, height=400).generate(investors)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Footer with Dataset Link and Your Name
st.markdown("""
    <div class="footer">
        Dataset used: <a href="https://www.kaggle.com/datasets/infodatalab/indian-unicorn-startups-2023" target="_blank">Indian Unicorn Startups 2023</a><br>
        Created by: [PSP]
    </div>
""", unsafe_allow_html=True)
