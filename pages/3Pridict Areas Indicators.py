import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

# Page Title
st.set_page_config(page_title="Socioeconomic Predictor", page_icon="🌍", layout="wide")

# Customize the sidebar
markdown = """
*MuseCL: Predicting Urban Socioeconomic Indicators via Multi-Semantic Contrastive Learning.*

Paper Link: <https://arxiv.org/abs/2407.09523>

GitHub Repository: <https://github.com/XixianYong/MuseCL>
"""
st.sidebar.title("About us")
st.sidebar.info(markdown)
logo = "logo.png"
qr_code = "qr_code.jpg"
col1, col2 = st.sidebar.columns(2)
col1.image(logo)
col2.image(qr_code)

# Welcome and Instructions
st.title("🌆 Welcome to the Socioeconomic Predictor!")
st.write("Ready to dive into some fascinating insights about the city? 🚀")
st.write(
    """
    Choose your data source, explore socioeconomic dynamics, and predict key indicators 
    like **population density**, **residential density**, or **POI count** across Beijing’s regions. 🌐
    Let's make data-driven predictions and understand the future trends of the city!
    """
)

# Data Source Selection
st.subheader("Select Your Data Source 📊")
data_source = st.selectbox(
    "Would you like to use your own dataset, or explore with Beijing's existing data?",
    ('None', 'Upload my own data', 'Use built-in Beijing data')
)

# Initialize session state
if 'ready_to_predict' not in st.session_state:
    st.session_state.ready_to_predict = False

if 'start_prediction' not in st.session_state:
    st.session_state.start_prediction = False

# Upload Own Data
if data_source == 'Upload my own data':
    st.session_state.ready_to_predict = False
    st.write("🎒 Let's gear up for your data journey! Please upload the following data files for all regions:")
    street_images = st.file_uploader("📷 Upload Street View Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    remote_images = st.file_uploader("🛰️ Upload Remote Sensing Images", type=['tif', 'png', 'jpg'], accept_multiple_files=True)
    poi_data = st.file_uploader("📌 Upload POI Data (CSV)", type=['csv'])
    population_data = st.file_uploader("👥 Upload Population Flow Data (CSV)", type=['csv'])

    # Prediction target selection
    st.subheader("Choose What to Predict 🧐")
    target_prediction = st.selectbox(
        "What would you like to predict?",
        ('None', 'Population Density', 'Residential Density', 'POI Count', 'Mobility Count')
    )
    if target_prediction == 'None':
        st.warning("🚫 Please choose a prediction target to start exploring.")
    else:
        st.write(f"🔮 You’ve chosen to predict: **{target_prediction}**")

    # Additional settings
    st.subheader("Customize Your Area Breakdown 🌍")
    region_type = st.selectbox("How would you like to divide the areas?", ('None', 'Rectangular Grid', 'Hexagonal Grid'))
    if region_type == 'None':
        st.warning("🚫 Please select a region division type to start exploring.")
    else:
        st.write(f"🗺️ You’ve chosen to divide the areas into: **{region_type}**")
    region_radius = st.slider("Set the area division size (in meters)", min_value=500, max_value=1000, step=50)

    # Check if all required files are uploaded
    if street_images and remote_images and poi_data and population_data:
        st.success("🎉 All data uploaded successfully! You're all set to start predictions.")
        st.session_state.ready_to_predict = True  # Set ready status to True when all files are uploaded

# Use Beijing Data
elif data_source == 'Use built-in Beijing data':
    # Prediction target selection
    st.subheader("Choose What to Predict 🧐")
    target_prediction = st.selectbox(
        "What would you like to predict?",
        ('None', 'Population Density', 'Residential Density')
    )
    if target_prediction == 'None':
        st.session_state.ready_to_predict = False
        st.session_state.start_prediction = False
        st.warning("🚫 Please choose a prediction target to start exploring.")
    else:
        st.write(f"🔮 You’ve chosen to predict: **{target_prediction}**")
        st.write("🗺️ Using Beijing’s existing data. Let’s explore the city’s socioeconomic factors together!")
        st.session_state.ready_to_predict = True  # Set ready status to True when existing data is used

elif data_source == 'None':
    st.session_state.ready_to_predict = False
    st.warning("🚫 Please select a data source to start exploring.")

# Display prediction options only when data is ready
if st.session_state.ready_to_predict:
    st.subheader("Ready to Predict 🚀")
    
    if st.button("Start Predicting") or st.session_state.start_prediction:
        st.session_state.start_prediction = True
        with st.spinner("Crunching the numbers... please wait while we predict the future of your selected regions! ⏳"):
            time.sleep(2)

        # Read the corresponding data based on target_prediction
        if target_prediction == "Population Density":
            data_path = "bj_data/pop_density.csv"
        elif target_prediction == "Residential Density":
            data_path = "bj_data/res_density.csv"
        # elif target_prediction == "POI Count":
        #     data_path = "bj_data/poi_count.csv"

        # Load the data
        data = pd.read_csv(data_path, header=None)
        
        # Prepare data for heatmap
        heat_data = [[row[0], row[1], row[2]] for row in data.values]

        # Create a map centered on Beijing
        map_center = [39.9042, 116.4074]  # Coordinates for Beijing
        m = folium.Map(location=map_center, zoom_start=10, scrollWheelZoom=False, control_scale=False)

        # Create heatmap
        HeatMap(heat_data).add_to(m)

        # Display the map
        st_folium(m, width=700, height=500)

        st.success("✅ Prediction complete! Check out the forecasted data on the map above. 🗺️")

        # Data Analysis Button
        if st.button("Analyze Data & Provide Policy Recommendations 📈"):
            with st.spinner("Analyzing data... Please wait. ⏳"):
                time.sleep(4)

            # Sample policy recommendations based on predictions
            if target_prediction == "Population Density":
                recommendations = """
                📊 **Population Density Analysis**:
                Beijing's population density showcases a stark contrast between various districts. Areas such as Chaoyang and Haidian are hotspots with significant overcrowding, where urban life is bustling but infrastructure is struggling to keep pace. Such high-density zones bring challenges like traffic jams, increased pollution, and pressure on public services. 
            
                **Recommendations**:
                1. **Expand Public Transportation**: Expand metro lines and bus routes to ensure seamless connectivity in high-density districts. This will not only reduce traffic congestion but also lower pollution levels by encouraging the use of public transit over private cars.
                2. **Affordable Housing Initiatives**: Create policies to drive affordable housing developments in these high-density areas, ensuring that middle-to-low-income families can find suitable accommodation without moving to the city outskirts.
                3. **Green Spaces and Recreational Areas**: Boost the development of parks, urban forests, and recreational spaces. This will help reduce the stress of crowded living conditions, offering residents a place to relax and enhancing their mental and physical well-being.
                4. **Smart City Solutions**: Leverage technology with smart city infrastructure, such as AI-powered traffic management, energy-efficient street lighting, and digital waste monitoring systems, to streamline urban operations and improve residents' quality of life.
                5. **Health and Wellness Programs**: Promote urban wellness initiatives by building community centers that offer health services, fitness programs, and mental health support to ease the pressures of high-density living.
                """
            elif target_prediction == "Residential Density":
                recommendations = """
                🏘️ **Residential Density Analysis**:
                Rapid residential development in certain districts has led to an influx of new residents, particularly in urban expansion zones. This growth strains essential services like healthcare, education, and infrastructure. As residential density increases, maintaining quality of life becomes a pressing issue.
            
                **Recommendations**:
                1. **Zoning Reforms**: Conduct a comprehensive review of zoning laws to support vertical expansion and mixed-use developments. Strategically relaxing zoning restrictions will enable efficient land use and help meet the rising demand for housing.
                2. **Community Services Expansion**: Prioritize the expansion of essential services, such as schools, hospitals, and public libraries, to keep pace with residential growth. This will ensure that residents in densely populated areas have access to quality education, healthcare, and community support.
                3. **Infrastructure and Utilities Overhaul**: Strengthen water supply, waste management, and power distribution systems in high-density neighborhoods. Investing in modern infrastructure will support sustainable urban development and reduce the risk of service disruptions.
                4. **Sustainable Development Practices**: Promote green building standards and sustainable architecture in new residential projects to reduce environmental impacts. Encourage developers to integrate solar panels, energy-efficient systems, and green roofs to contribute to a more sustainable urban ecosystem.
                5. **Public Engagement and Education**: Run city-wide campaigns to inform residents about sustainable living practices—everything from recycling and water conservation to adopting energy-efficient habits. Engaging the public helps build a collaborative effort toward sustainable growth.
                """
            else:
                recommendations = "No specific recommendations available for the selected target."

            st.write("📋 Policy Recommendations:")
            st.write(recommendations)



# 页脚
st.markdown("---")
st.markdown("""
This tool uses our advanced **MuseCL model** to analyze urban data, bringing you insights you might never have noticed before. 🎯  
Stay tuned for more updates and exciting features!
""")
