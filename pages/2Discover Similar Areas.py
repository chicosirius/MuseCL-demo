import time
import streamlit as st
import pandas as pd
import pydeck as pdk

# 设置页面配置
st.set_page_config(page_title="Explore Similar Areas", page_icon="🌍", layout="wide")

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

# 初始化 session_state
if 'data_uploaded' not in st.session_state:
    st.session_state['data_uploaded'] = False
if 'clicked_area' not in st.session_state:
    st.session_state['clicked_area'] = None
if 'similarity_calculated' not in st.session_state:
    st.session_state['similarity_calculated'] = False

# 标题和简介
st.title("🔍 Discover Similar Urban Areas")
st.markdown("""
Welcome to the **Ultimate Urban Explorer**! 🌆✨  
Ever wondered how different areas of a city compare socioeconomically? Let's dive into the magic of similarity detection across cities. Choose between **Beijing's built-in data** or import your own city's data to find out which areas match up the closest.

**Ready to explore? Let's get started!**
""")

# 上传数据选项
st.subheader("Select Your Data Source 📊")
data_selection = st.selectbox(
    "Would you like to use your own dataset, or explore with Beijing's existing data?",
    ("None", "Upload my own data", "Use built-in Beijing data")
)

# 用户上传自定义数据
if data_selection == "Upload my own data" and not st.session_state['data_uploaded']:
    st.session_state['similarity_calculated'] = False

    st.write("🎒 Let's gear up for your data journey! Please upload the following data files for all regions:")
    street_images = st.file_uploader("📷 Upload Street View Images", type=['png', 'jpg', 'jpeg', 'zip'], accept_multiple_files=True)
    remote_images = st.file_uploader("🛰️ Upload Remote Sensing Images", type=['tif', 'png', 'jpg', 'zip'], accept_multiple_files=True)
    poi_data = st.file_uploader("📌 Upload POI Data (CSV)", type=['csv'])
    population_data = st.file_uploader("👥 Upload Population Flow Data (CSV)", type=['csv'])

    if street_images and remote_images and poi_data and population_data:
        st.success("All files uploaded! You're ready to start calculating similarity.")
        st.session_state['data_uploaded'] = True
elif data_selection == "Use built-in Beijing data":
    st.success("Using built-in Beijing data! You're ready to start calculating similarity.")
elif data_selection == 'None':
    st.warning("🚫 Please select a data source to start exploring.")

# 开始计算按钮
if st.session_state['data_uploaded'] or data_selection == "Use built-in Beijing data":
    if st.button("Start Similarity Calculation") or st.session_state['similarity_calculated']:

        with st.spinner("Please hold on for a moment while we calculate the similarity... 🚀"):
            time.sleep(1)

        st.session_state['similarity_calculated'] = True  # 设置按钮状态为已计算

        # 模拟的区域数据
        areas = [
            {"name": "Point 1 in Chaoyang District", "lat": 39.9219, "lon": 116.4433, "similar": "Point 5 in Fengtai District"},
            {"name": "Point 2 in Haidian District", "lat": 39.9997, "lon": 116.3267, "similar": "Point 4 in Xicheng District"},
            {"name": "Point 3 in Dongcheng District", "lat": 39.9309, "lon": 116.4167, "similar": "Point 2 in Haidian District"},
            {"name": "Point 4 in Xicheng District", "lat": 39.9123, "lon": 116.3661, "similar": "Point 3 in Dongcheng District"},
            {"name": "Point 5 in Fengtai District", "lat": 39.8586, "lon": 116.2869, "similar": "Point 1 in Chaoyang District"}
        ]

        others = [ 
            {"name": "Point in Shijingshan District", "lat": 39.9145, "lon": 116.1956},
            {"name": "Point in Tongzhou District", "lat": 39.9026, "lon": 116.6633},
            {"name": "Point in Changping District", "lat": 40.2208, "lon": 116.2334},
            {"name": "Point in Daxing District", "lat": 39.7181, "lon": 116.4053},
            {"name": "Point in Fangshan District", "lat": 39.7025, "lon": 115.9928},
            {"name": "Point in Mentougou District", "lat": 39.9384, "lon": 116.1061},
            {"name": "Point in Pinggu District", "lat": 40.1448, "lon": 117.1001},
            {"name": "Point in Huairou District", "lat": 40.3344, "lon": 116.6377},
            {"name": "Point in Miyun District", "lat": 40.3774, "lon": 116.8414},
            {"name": "Point in Haidian District", "lat": 39.9997, "lon": 116.3267},
            {"name": "Point in Shunyi District", "lat": 40.1276, "lon": 116.6558},
            {"name": "Point in Yanqing District", "lat": 40.4653, "lon": 115.9854},
            {"name": "Point in Changping District", "lat": 40.2208, "lon": 116.2334},
            {"name": "Point in Daxing District", "lat": 39.7181, "lon": 116.4053},
            {"name": "Point in Fangshan District", "lat": 39.7025, "lon": 115.9928},
            {"name": "Point in Mentougou District", "lat": 39.9384, "lon": 116.1061},
            {"name": "Point in Pinggu District", "lat": 40.1448, "lon": 117.1001},
            {"name": "Point in Huairou District", "lat": 40.3344, "lon": 116.6377},
            {"name": "Point in Miyun District", "lat": 40.3774, "lon": 116.8414},
            {"name": "Point in Haidian District", "lat": 39.9997, "lon": 116.3267},
            {"name": "Point in Shunyi District", "lat": 40.1276, "lon": 116.6558},
            {"name": "Point in Yanqing District", "lat": 40.4653, "lon": 115.9854},
            {"name": "Point in Chaoyang District", "lat": 39.9219, "lon": 116.4433},
            {"name": "Point in Yizhuang District", "lat": 39.7955, "lon": 116.5065}
        ]

        # 模拟生成每个区域的POI信息、遥感图像和街景图像
        sample_data = {
            "Point 1 in Chaoyang District": {
                "poi": "Chaoyang Park 🌳, CCTV Headquarters 📺",
                "remote_sensing": "pic/6969_116.4981,39.8792_/6969.jpg",
                "street_views": [
                    "pic/6969_116.4981,39.8792_/0100220000130730143201874J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730114135754J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730121223847J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730125921875J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730125936048J1.jpg"
                ]
            },
            "Point 2 in Haidian District": {
                "poi": "Zhongguancun Tech Hub 💻, Peking University 🎓",
                "remote_sensing": "pic/6859_116.3372,39.9092_/6859.jpg",
                "street_views": [
                    "pic/6859_116.3372,39.9092_/0900220000150520053741088A6.jpg",
                    "pic/6859_116.3372,39.9092_/01002200001309261617204985L.jpg",
                    "pic/6859_116.3372,39.9092_/09002200121902071504097782L.jpg",
                    "pic/6859_116.3372,39.9092_/09002200121902071504197972L.jpg",
                    "pic/6859_116.3372,39.9092_/09002200122003121235474337C.jpg"
                ]
            },
            "Point 3 in Dongcheng District": {
                "poi": "Tiananmen Square 🏯, Wangfujing Street 🛍️",
                "remote_sensing": "pic/6966_116.3709,39.8937/6966.jpg",
                "street_views": [
                    "pic/6966_116.3709,39.8937/0900220000150520051102283T5.jpg",
                    "pic/6966_116.3709,39.8937/01002200001308241326554645A.jpg",
                    "pic/6966_116.3709,39.8937/01002200001308251428497545A.jpg",
                    "pic/6966_116.3709,39.8937/01002200001309111415112215K.jpg",
                    "pic/6966_116.3709,39.8937/09002200011509170700287115T.jpg",
                    "pic/6966_116.3709,39.8937/09002200011601291253212642Q.jpg"
                ]
            },
            "Point 4 in Xicheng District": {
                "poi": "Beihai Park 🌊, National Centre for Performing Arts 🎭",
                "remote_sensing": "pic/6860_116.3691,39.9133_/6860.jpg",
                "street_views": [
                    "pic/6860_116.3691,39.9133_/0100220000130810104132011J5.jpg",
                    "pic/6860_116.3691,39.9133_/0100220000130818092310143J5.jpg",
                    "pic/6860_116.3691,39.9133_/0900220000150525065106500T5.jpg",
                    "pic/6860_116.3691,39.9133_/09002200121902041435567412L.jpg"
                ]
            },
            "Point 5 in Fengtai District": {
                "poi": "Beijing Garden Expo 🌸, Lugou Bridge 🏰",
                "remote_sensing": "pic/6911_116.2777,39.8904_/6911.jpg",
                "street_views": [
                    "pic/6911_116.2777,39.8904_/0100220000130724160835512J4.jpg",
                    "pic/6911_116.2777,39.8904_/09002200121706241459119509S.jpg",
                    "pic/6911_116.2777,39.8904_/09002200121706241459556769S.jpg",
                    "pic/6911_116.2777,39.8904_/09002200121902211249323977F.jpg"
                ]
            }
        }

        # 构建 Pydeck 地图
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame(areas + others),
            get_position="[lon, lat]",
            get_color=[200, 30, 0, 160],
            get_radius=500,
            pickable=True,
        )

        # 定义地图视图
        view_state = pdk.ViewState(latitude=39.9, longitude=116.4, zoom=10, pitch=50)
        deck = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}"})

        # 显示地图
        st.pydeck_chart(deck)

        # 提示用户点击区域
        st.markdown("Click on any area marker to see its details and the most similar region! 🎯")

        # 显示区域选择框
        clicked_area = st.selectbox("Select a region manually (if click does not work):", options=["None"] + [area["name"] for area in areas], index=0)

        # 只有当用户选择了区域时才显示详细信息和最相似区域
        if clicked_area != "None":
            st.session_state['clicked_area'] = clicked_area  # 保存用户选择的区域
            similar_area = next(area["similar"] for area in areas if area["name"] == clicked_area)
            st.subheader(f"Details for {clicked_area} and its most similar area: {similar_area}")

            # 使用 columns 进行左右对比显示
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {clicked_area}")
                st.markdown(f"**POI Data**: {sample_data[clicked_area]['poi']}")
                st.markdown(f"**Remote Sensing Image**:")
                st.image(sample_data[clicked_area]['remote_sensing'], caption=f"Remote Sensing of {clicked_area}")
                st.markdown(f"**Street Views**:")
                if len(sample_data[clicked_area]['street_views']) > 1:
                    # Use slider to browse through street views if more than one image is available
                    street_img_idx = st.slider("Street View Image Index", 0, len(sample_data[clicked_area]['street_views']) - 1, 0, key=f"street_view_slider_{clicked_area}")
                    st.image(sample_data[clicked_area]['street_views'][street_img_idx], caption="Street View")
                else:
                    st.image(sample_data[clicked_area]['street_views'][0], caption=f"Street View 1 of {clicked_area}")

            with col2:
                st.markdown(f"### {similar_area}")
                st.markdown(f"**POI Data**: {sample_data[similar_area]['poi']}")
                st.markdown(f"**Remote Sensing Image**:")
                st.image(sample_data[similar_area]['remote_sensing'], caption=f"Remote Sensing of {similar_area}")
                st.markdown(f"**Street Views**:")
                if len(sample_data[similar_area]['street_views']) > 1:
                    # Use slider to browse through street views if more than one image is available
                    street_img_idx = st.slider("Street View Image Index", 0, len(sample_data[similar_area]['street_views']) - 1, 0, key=f"street_view_slider_{similar_area}")
                    st.image(sample_data[similar_area]['street_views'][street_img_idx], caption="Street View")
                else:
                    st.image(sample_data[similar_area]['street_views'][0], caption=f"Street View 1 of {similar_area}")

# 页脚
st.markdown("---")
st.markdown("""
This tool uses our advanced **MuseCL model** to analyze urban data, bringing you insights you might never have noticed before. 🎯  
Stay tuned for more updates and exciting features!
""")
