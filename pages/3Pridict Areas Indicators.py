# import streamlit as st
# import pandas as pd
# import folium
# from folium.plugins import HeatMap
# from streamlit_folium import st_folium
# import time

# # Page Title
# st.set_page_config(page_title="Socioeconomic Predictor", page_icon="🌍", layout="wide")

# # Customize the sidebar
# markdown = """
# *MuseCL: Predicting Urban Socioeconomic Indicators via Multi-Semantic Contrastive Learning.*

# Paper Link: <https://arxiv.org/abs/2407.09523>

# GitHub Repository: <https://github.com/XixianYong/MuseCL>
# """
# st.sidebar.title("About us")
# st.sidebar.info(markdown)
# logo = "logo.png"
# qr_code = "qr_code.jpg"
# col1, col2 = st.sidebar.columns(2)
# col1.image(logo)
# col2.image(qr_code)

# # Welcome and Instructions
# st.title("🌆 Welcome to the Socioeconomic Predictor!")
# st.write("Ready to dive into some fascinating insights about the city? 🚀")
# st.write(
#     """
#     Choose your data source, explore socioeconomic dynamics, and predict key indicators 
#     like **population density**, **residential density**, or **POI count** across Beijing’s regions. 🌐
#     Let's make data-driven predictions and understand the future trends of the city!
#     """
# )

# # Data Source Selection
# st.subheader("Select Your Data Source 📊")
# data_source = st.selectbox(
#     "Would you like to use your own dataset, or explore with Beijing's existing data?",
#     ('None', 'Upload my own data', 'Use built-in Beijing data')
# )

# # Initialize session state
# if 'ready_to_predict' not in st.session_state:
#     st.session_state.ready_to_predict = False

# if 'start_prediction' not in st.session_state:
#     st.session_state.start_prediction = False

# # Upload Own Data
# if data_source == 'Upload my own data':
#     st.session_state.ready_to_predict = False
#     st.write("🎒 Let's gear up for your data journey! Please upload the following data files for all regions:")
#     street_images = st.file_uploader("📷 Upload Street View Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
#     remote_images = st.file_uploader("🛰️ Upload Remote Sensing Images", type=['tif', 'png', 'jpg'], accept_multiple_files=True)
#     poi_data = st.file_uploader("📌 Upload POI Data (CSV)", type=['csv'])
#     population_data = st.file_uploader("👥 Upload Population Flow Data (CSV)", type=['csv'])

#     # Prediction target selection
#     st.subheader("Choose What to Predict 🧐")
#     target_prediction = st.selectbox(
#         "What would you like to predict?",
#         ('None', 'Population Density', 'Residential Density', 'POI Count', 'Mobility Count')
#     )
#     if target_prediction == 'None':
#         st.warning("🚫 Please choose a prediction target to start exploring.")
#     else:
#         st.write(f"🔮 You’ve chosen to predict: **{target_prediction}**")

#     # Additional settings
#     st.subheader("Customize Your Area Breakdown 🌍")
#     region_type = st.selectbox("How would you like to divide the areas?", ('None', 'Rectangular Grid', 'Hexagonal Grid'))
#     if region_type == 'None':
#         st.warning("🚫 Please select a region division type to start exploring.")
#     else:
#         st.write(f"🗺️ You’ve chosen to divide the areas into: **{region_type}**")
#     region_radius = st.slider("Set the area division size (in meters)", min_value=500, max_value=1000, step=50)

#     # Check if all required files are uploaded
#     if street_images and remote_images and poi_data and population_data:
#         st.success("🎉 All data uploaded successfully! You're all set to start predictions.")
#         st.session_state.ready_to_predict = True  # Set ready status to True when all files are uploaded

# # Use Beijing Data
# elif data_source == 'Use built-in Beijing data':
#     # Prediction target selection
#     st.subheader("Choose What to Predict 🧐")
#     target_prediction = st.selectbox(
#         "What would you like to predict?",
#         ('None', 'Population Density', 'Residential Density')
#     )
#     if target_prediction == 'None':
#         st.session_state.ready_to_predict = False
#         st.session_state.start_prediction = False
#         st.warning("🚫 Please choose a prediction target to start exploring.")
#     else:
#         st.write(f"🔮 You’ve chosen to predict: **{target_prediction}**")
#         st.write("🗺️ Using Beijing’s existing data. Let’s explore the city’s socioeconomic factors together!")
#         st.session_state.ready_to_predict = True  # Set ready status to True when existing data is used

# elif data_source == 'None':
#     st.session_state.ready_to_predict = False
#     st.warning("🚫 Please select a data source to start exploring.")

# # Display prediction options only when data is ready
# if st.session_state.ready_to_predict:
#     st.subheader("Ready to Predict 🚀")
    
#     if st.button("Start Predicting") or st.session_state.start_prediction:
#         st.session_state.start_prediction = True
#         with st.spinner("Crunching the numbers... please wait while we predict the future of your selected regions! ⏳"):
#             time.sleep(2)

#         # Read the corresponding data based on target_prediction
#         if target_prediction == "Population Density":
#             data_path = "bj_data/pop_density.csv"
#         elif target_prediction == "Residential Density":
#             data_path = "bj_data/res_density.csv"
#         # elif target_prediction == "POI Count":
#         #     data_path = "bj_data/poi_count.csv"

#         # Load the data
#         data = pd.read_csv(data_path, header=None)
        
#         # Prepare data for heatmap
#         heat_data = [[row[0], row[1], row[2]] for row in data.values]

#         # Create a map centered on Beijing
#         map_center = [39.9042, 116.4074]  # Coordinates for Beijing
#         m = folium.Map(location=map_center, zoom_start=10, scrollWheelZoom=False, control_scale=False)

#         # Create heatmap
#         HeatMap(heat_data).add_to(m)

#         # Display the map
#         st_folium(m, width=700, height=500)

#         st.success("✅ Prediction complete! Check out the forecasted data on the map above. 🗺️")

#         # Data Analysis Button
#         if st.button("Analyze Data & Provide Policy Recommendations 📈"):
#             with st.spinner("Analyzing data... Please wait. ⏳"):
#                 time.sleep(4)

#             # Sample policy recommendations based on predictions
#             if target_prediction == "Population Density":
#                 recommendations = """
#                 📊 **Population Density Analysis**:
#                 Beijing's population density showcases a stark contrast between various districts. Areas such as Chaoyang and Haidian are hotspots with significant overcrowding, where urban life is bustling but infrastructure is struggling to keep pace. Such high-density zones bring challenges like traffic jams, increased pollution, and pressure on public services. 
            
#                 **Recommendations**:
#                 1. **Expand Public Transportation**: Expand metro lines and bus routes to ensure seamless connectivity in high-density districts. This will not only reduce traffic congestion but also lower pollution levels by encouraging the use of public transit over private cars.
#                 2. **Affordable Housing Initiatives**: Create policies to drive affordable housing developments in these high-density areas, ensuring that middle-to-low-income families can find suitable accommodation without moving to the city outskirts.
#                 3. **Green Spaces and Recreational Areas**: Boost the development of parks, urban forests, and recreational spaces. This will help reduce the stress of crowded living conditions, offering residents a place to relax and enhancing their mental and physical well-being.
#                 4. **Smart City Solutions**: Leverage technology with smart city infrastructure, such as AI-powered traffic management, energy-efficient street lighting, and digital waste monitoring systems, to streamline urban operations and improve residents' quality of life.
#                 5. **Health and Wellness Programs**: Promote urban wellness initiatives by building community centers that offer health services, fitness programs, and mental health support to ease the pressures of high-density living.
#                 """
#             elif target_prediction == "Residential Density":
#                 recommendations = """
#                 🏘️ **Residential Density Analysis**:
#                 Rapid residential development in certain districts has led to an influx of new residents, particularly in urban expansion zones. This growth strains essential services like healthcare, education, and infrastructure. As residential density increases, maintaining quality of life becomes a pressing issue.
            
#                 **Recommendations**:
#                 1. **Zoning Reforms**: Conduct a comprehensive review of zoning laws to support vertical expansion and mixed-use developments. Strategically relaxing zoning restrictions will enable efficient land use and help meet the rising demand for housing.
#                 2. **Community Services Expansion**: Prioritize the expansion of essential services, such as schools, hospitals, and public libraries, to keep pace with residential growth. This will ensure that residents in densely populated areas have access to quality education, healthcare, and community support.
#                 3. **Infrastructure and Utilities Overhaul**: Strengthen water supply, waste management, and power distribution systems in high-density neighborhoods. Investing in modern infrastructure will support sustainable urban development and reduce the risk of service disruptions.
#                 4. **Sustainable Development Practices**: Promote green building standards and sustainable architecture in new residential projects to reduce environmental impacts. Encourage developers to integrate solar panels, energy-efficient systems, and green roofs to contribute to a more sustainable urban ecosystem.
#                 5. **Public Engagement and Education**: Run city-wide campaigns to inform residents about sustainable living practices—everything from recycling and water conservation to adopting energy-efficient habits. Engaging the public helps build a collaborative effort toward sustainable growth.
#                 """
#             else:
#                 recommendations = "No specific recommendations available for the selected target."

#             st.write("📋 Policy Recommendations:")
#             st.write(recommendations)



# # 页脚
# st.markdown("---")
# st.markdown("""
# This tool uses our advanced **MuseCL model** to analyze urban data, bringing you insights you might never have noticed before. 🎯  
# Stay tuned for more updates and exciting features!
# """)

import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

# Page Title
st.set_page_config(page_title="Socioeconomic Predictor", page_icon="🌍", layout="wide")

# 自定义侧边栏
markdown = """
*MuseCL: 通过多语义对比学习预测城市社会经济指标*

论文链接: <https://arxiv.org/abs/2407.09523>

GitHub 仓库: <https://github.com/XixianYong/MuseCL>
"""
st.sidebar.title("关于我们")
st.sidebar.info(markdown)
logo = "logo.png"
qr_code = "qr_code.jpg"
col1, col2 = st.sidebar.columns(2)
col1.image(logo)
col2.image(qr_code)

# 欢迎和说明
st.title("🌆 欢迎来到社会经济预测工具")
st.write("准备好探索一些关于这座城市的精彩见解了吗？🚀")
st.write(
    """
    选择您的数据源，探索社会经济动态，并预测关键指标，
    如 **人口密度**、**居住密度** 或 **POI 数量**，覆盖北京的各个区域。🌐
    让我们通过数据驱动的预测，了解这座城市的未来趋势吧！
    """
)

# 数据源选择
st.subheader("选择您的数据源 📊")
data_source = st.selectbox(
    "您是想使用自己的数据集，还是探索北京的现有数据？",
    ('无', '上传我自己的数据', '使用内置的北京数据')
)

# 初始化会话状态
if 'ready_to_predict' not in st.session_state:
    st.session_state.ready_to_predict = False

if 'start_prediction' not in st.session_state:
    st.session_state.start_prediction = False

# 上传自己的数据
if data_source == '上传我自己的数据':
    st.session_state.ready_to_predict = False
    st.write("🎒 准备好开始您的数据之旅吧！请上传以下所有区域的数据文件：")
    street_images = st.file_uploader("📷 上传街景图片", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
    remote_images = st.file_uploader("🛰️ 上传遥感图像", type=['tif', 'png', 'jpg'], accept_multiple_files=True)
    poi_data = st.file_uploader("📌 上传POI数据 (CSV)", type=['csv'])
    population_data = st.file_uploader("👥 上传人口流动数据 (CSV)", type=['csv'])

    # 预测目标选择
    st.subheader("选择预测内容 🧐")
    target_prediction = st.selectbox(
        "您想预测什么？",
        ('无', '人口密度', '居住密度', 'POI 数量', '流动人口数量')
    )
    if target_prediction == '无':
        st.warning("🚫 请选择一个预测目标以开始探索。")
    else:
        st.write(f"🔮 您选择了预测：**{target_prediction}**")

    # 额外设置
    st.subheader("自定义区域划分 🌍")
    region_type = st.selectbox("您想如何划分区域？", ('无', '矩形网格', '六边形网格'))
    if region_type == '无':
        st.warning("🚫 请选择一个区域划分方式以开始探索。")
    else:
        st.write(f"🗺️ 您选择了将区域划分为：**{region_type}**")
    region_radius = st.slider("设置区域划分大小（以米为单位）", min_value=500, max_value=1000, step=50)

    # 检查是否已上传所有必需的文件
    if street_images and remote_images and poi_data and population_data:
        st.success("🎉 所有数据上传成功！您可以开始预测了。")
        st.session_state.ready_to_predict = True  # 当所有文件上传完毕后，将状态设置为True

# 使用北京数据
elif data_source == '使用内置的北京数据':
    # 预测目标选择
    st.subheader("选择预测内容 🧐")
    target_prediction = st.selectbox(
        "您想预测什么？",
        ('无', '人口密度', '居住密度')
    )
    if target_prediction == '无':
        st.session_state.ready_to_predict = False
        st.session_state.start_prediction = False
        st.warning("🚫 请选择一个预测目标以开始探索。")
    else:
        st.write(f"🔮 您选择了预测：**{target_prediction}**")
        st.write("🗺️ 使用北京的现有数据。让我们一起探索这座城市的社会经济因素吧！")
        st.session_state.ready_to_predict = True  # 当使用现有数据时，将状态设置为True

elif data_source == '无':
    st.session_state.ready_to_predict = False
    st.warning("🚫 请选择一个数据源以开始探索。")

# 仅在数据准备好时显示预测选项
if st.session_state.ready_to_predict:
    st.subheader("准备开始预测 🚀")
    
    if st.button("开始预测") or st.session_state.start_prediction:
        st.session_state.start_prediction = True
        with st.spinner("正在处理数据... 请稍等，系统正在预测您选择的区域的未来！⏳"):
            time.sleep(4)

        # 根据 target_prediction 读取相应的数据
        if target_prediction == "人口密度":
            data_path = "bj_data/pop_density.csv"
        elif target_prediction == "居住密度":
            data_path = "bj_data/res_density.csv"
        # elif target_prediction == "POI 数量":
        #     data_path = "bj_data/poi_count.csv"

        # 加载数据
        data = pd.read_csv(data_path, header=None)
        
        # 准备数据用于热力图
        heat_data = [[row[0], row[1], row[2]] for row in data.values]

        # 创建一个以北京为中心的地图
        map_center = [39.9042, 116.4074]  # 北京的坐标
        m = folium.Map(location=map_center, zoom_start=10, scrollWheelZoom=False, control_scale=False)

        # 创建热力图
        HeatMap(heat_data).add_to(m)

        # 显示地图
        st_folium(m, width=700, height=500)

        st.success("✅ 预测完成！请查看上方地图中的预测数据。🗺️")

        # 数据分析按钮
        if st.button("分析数据并提供政策建议 📈"):
            with st.spinner("正在分析数据... 请稍候。⏳"):
                time.sleep(4)

            # 根据预测提供样本政策建议
            if target_prediction == "人口密度":
                recommendations = """
                1. **增加公共交通**：改善公共交通线路以应对日益增加的人口密度。
                2. **可负担住房计划**：实施政策，鼓励在高密度地区开发可负担住房。
                3. **绿色空间开发**：创建更多公园和休闲区域，以提高人口密集社区的生活质量。
                """
            elif target_prediction == "居住密度":
                recommendations = """
                1. **调整土地规划**：重新评估土地规划法规，以允许在合适的区域进行高密度开发。
                2. **扩展社区服务**：在居住密集的区域扩展社区服务，如学校和医院。
                3. **基础设施改进**：投资基础设施改进，以支持更高的居住密度，包括公用设施和道路网络。
                """
            else:
                recommendations = "对于所选目标暂无具体建议。"

            st.write("📋 政策建议：")
            st.write(recommendations)

# 页脚
st.markdown("---")
st.markdown("""
此工具使用我们先进的 **MuseCL 模型** 来分析城市数据，带给您前所未有的见解。🎯  
请继续关注更多更新和令人兴奋的功能！
""")

