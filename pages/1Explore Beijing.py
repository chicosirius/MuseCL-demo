import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import random

# 设置页面配置
st.set_page_config(page_title="Explore Urban Data", page_icon="🌍", layout="wide")

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

# Path for images
image_path = "/Users/sirius/Desktop/MuseCL-demo/square.jpg"

beijing_points = {
    'Point 1': {'coords': [40.0613, 116.5592], 
                'remote_img': "pic/5964_116.5592,40.0613/5964.jpg", 
                'street_imgs': ["pic/5964_116.5592,40.0613/09002200121706210912468954C.jpg", 
                                "pic/5964_116.5592,40.0613/09002200121706210925270234C.jpg", 
                                "pic/5964_116.5592,40.0613/09002200121706211009087794C.jpg", 
                                "pic/5964_116.5592,40.0613/09002200121902151409592358O.jpg", 
                                "pic/5964_116.5592,40.0613/09002200121902151640198768O.jpg", 
                                "pic/5964_116.5592,40.0613/09002200121902151646132208O.jpg"], 
                'poi_info': 'This area is a dynamic **commercial district**, teeming with **shopping malls**, trendy **cafes**, and **entertainment venues**. It\'s perfect for tourists and locals alike seeking the vibrant pulse of modern Beijing. 🌆🛍️'},

}

# Function to add markers
def add_markers_to_map(map_obj, points):
    for point, data in points.items():
        folium.Marker(location=data['coords'], popup=point, tooltip=point).add_to(map_obj)

# Initialize session state for user-added points
if 'custom_points' not in st.session_state:
    st.session_state.custom_points = []

# Generate random POI points within a certain bounding box (Beijing region)
def generate_random_pois(n=200, lat_center=39.90, lon_center=116.40, lat_std=0.03, lon_std=0.05):
    pois = []
    for _ in range(n):
        # 使用正态分布生成 POI，均值为城区中心坐标，标准差控制偏离程度
        lat = random.gauss(lat_center, lat_std)
        lon = random.gauss(lon_center, lon_std)
        pois.append([lat, lon])
    return pois

# Check if the random POIs are already generated
if 'poi_categories' not in st.session_state:
    # Initialize POI data for different categories once
    st.session_state.poi_categories = {
        "Restaurants": generate_random_pois(n=500),
        "Entertainment": generate_random_pois(n=200),
        "Cultural": generate_random_pois(n=80)
    }

# Page layout
st.title("🗺️ Explore Beijing - Discover the Heart of China!")
st.write("""
Welcome to **Beijing**, the bustling capital of China, where ancient culture meets modern innovation!

Here, you can explore different districts of this vibrant city through satellite views, street images, and key Points of Interest (POI). Whether it's historical sites, busy marketplaces, or quiet residential areas, each part of Beijing tells a unique story. Let’s embark on this journey! 🌏✨
""")

# Add guiding statements with emojis
st.markdown("""
### How to explore the map? 🧭
1. **Navigate the map**: Move around, zoom in, or zoom out to explore different areas of Beijing.
2. **Click on a marker**: Select one of the marked points to uncover more about that specific area, from its satellite view to street-level insights.
3. **Check the details**: After clicking a marker, information about that region will appear to the right. You’ll see satellite views, street photos, and local hotspots or historical landmarks.

🔍 **Tip**: Want to learn more about the heart of Beijing or explore hidden gems? Just click on any marker and let the city’s charm reveal itself!
""")

# Add a brief intro about Beijing’s culture and landmarks
st.write("""
### A Glimpse of Beijing’s Magic 🏛️
Beijing isn’t just the political center of China, it’s also home to rich historical landmarks such as the **Forbidden City**, **Tiananmen Square**, and **the Summer Palace**. 
Beyond these, the city is brimming with traditional hutongs, modern skyscrapers, and cultural heritage, creating a fascinating blend of old and new.
Each corner of the city holds something special, whether it’s a bustling market, serene park, or quiet residential alley.

Now, let’s explore the diverse regions of Beijing! 🌆
""")

# Create layout with two columns
col1, col2 = st.columns([2, 1])

# Left column: display the map
with col1:
    # Initialize map centered on Beijing
    m = folium.Map(location=[39.9042, 116.4074], zoom_start=11)

    # Add markers for predefined points
    add_markers_to_map(m, beijing_points)
    # Add custom points from session state
    for custom_point in st.session_state.custom_points:
        folium.Marker(location=custom_point, popup="Custom Point", icon=folium.Icon(color='red')).add_to(m)


    # Add markers for each point
    for point_name, point_info in beijing_points.items():
        folium.Marker(location=point_info['coords'], popup=point_name).add_to(m)

    # User-added point feature
    user_lat = st.number_input("Enter Latitude:", min_value=39.0, max_value=41.0, value=39.9)
    user_lng = st.number_input("Enter Longitude:", min_value=115.0, max_value=117.0, value=116.4)
    
    if st.button("Add Custom Point"):
        # Append the custom point to session state
        st.session_state.custom_points.append([user_lat, user_lng])
        st.success(f"Added point at ({user_lat}, {user_lng})")

    # Add POI category filter
    poi_filter = st.selectbox("Filter POI Category:", ["None", "Restaurants", "Entertainment", "Cultural"])
    
    # Add 100 random POIs as a heatmap based on the category selection
    if poi_filter != "None":
        poi_points = st.session_state.poi_categories[poi_filter]
        heatmap = HeatMap(poi_points, radius=15, blur=10)
        heatmap.add_to(m)

    # Display the map
    map_data = st_folium(m, width=700, height=700)

# Right column: display details when a point is clicked
with col2:
    st.write("### Dive into the Details of the Area 🎯")
    
    # Show data when a point is clicked
    if map_data['last_object_clicked']:
        clicked_coords = map_data['last_object_clicked']['lat'], map_data['last_object_clicked']['lng']
        
        # Find and display the clicked point's information
        for point_name, point_info in beijing_points.items():
            if clicked_coords == tuple(point_info['coords']):
                st.subheader(f"Discover {point_name} 🌟")
                
                # Display POI information first
                st.write(f"**Points of Interest**: {point_info['poi_info']} 🏙️")
                
                # Display remote sensing image and street view images with same size
                st.write("**Remote Sensing Image 🛰️:**")
                st.image(point_info['remote_img'], caption="Satellite Image", use_column_width=True)

                st.write("**Street Views 🚶:**")
                # Check if there are multiple street view images
                if len(point_info['street_imgs']) > 1:
                    # Use slider to browse through street views if more than one image is available
                    street_img_idx = st.slider("Street View Image Index", 0, len(point_info['street_imgs']) - 1, 0)
                    st.image(point_info['street_imgs'][street_img_idx], caption="Street View", use_column_width=True)
                else:
                    # If only one image is available, display it directly
                    st.image(point_info['street_imgs'][0], caption="Street View", use_column_width=True)

    else:
        st.write("Click on a marker to reveal the area’s details on the right ⬅️.")

# Add a footer or final message
st.write("""
#### Ready to uncover more? 🧳
Whether you’re a history enthusiast, a city explorer, or simply curious, Beijing has something for everyone! 
Keep exploring the map, click on different points, and immerse yourself in this fascinating city’s different layers.
""")
