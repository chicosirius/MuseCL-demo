import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import random

# 设置页面配置
st.set_page_config(page_title="探索城市多模态数据", page_icon="🌍", layout="wide")

# Customize the sidebar
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

# Path for images
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
    
    'Point 2': {'coords': [39.8937, 116.3709], 
                'remote_img': "pic/6966_116.3709,39.8937/6966.jpg", 
                'street_imgs': ["pic/6966_116.3709,39.8937/0900220000150520051102283T5.jpg", 
                                "pic/6966_116.3709,39.8937/01002200001308241326554645A.jpg", 
                                "pic/6966_116.3709,39.8937/01002200001308251428497545A.jpg", 
                                "pic/6966_116.3709,39.8937/01002200001309111415112215K.jpg", 
                                "pic/6966_116.3709,39.8937/09002200011509170700287115T.jpg", 
                                "pic/6966_116.3709,39.8937/09002200011509170700287115T.jpg", 
                                "pic/6966_116.3709,39.8937/09002200011601291253212642Q.jpg"], 
                'poi_info': 'Known for its eclectic mix of **restaurants** and cozy **cafes**, this is the place to indulge in **local street food** and **international cuisine**. The area is a foodie’s paradise with both hidden gems and famous dining spots. 🍜🍣'},
    
    'Point 3': {'coords': [39.8006, 116.5614], 
                'remote_img': "pic/7448_116.5614,39.8006/7448.jpg", 
                'street_imgs': ["pic/7448_116.5614,39.8006/01002200001309050940555415X.jpg", 
                                "pic/7448_116.5614,39.8006/01002200001309050943086005X.jpg", 
                                "pic/7448_116.5614,39.8006/09002200121706201454219267E.jpg", 
                                "pic/7448_116.5614,39.8006/09002200121706201735485447E.jpg", 
                                "pic/7448_116.5614,39.8006/09002200121706210847152587E.jpg", 
                                "pic/7448_116.5614,39.8006/09002200121706210847172527E.jpg", 
                                "pic/7448_116.5614,39.8006/09002200121706211025085807E.jpg"], 
                'poi_info': 'A hub for **cultural attractions** and **artistic venues**, this area boasts **art galleries**, **museums**, and **theaters**. It’s the perfect spot for anyone wanting to dive into Beijing’s rich cultural heritage and contemporary arts scene. 🎭🎨'},
    
    'Point 4': {'coords': [39.7841, 116.4735], 
                'remote_img': "pic/7552_116.4735,39.7841/7552.jpg", 
                'street_imgs': ["pic/7552_116.4735,39.7841/01002200001308171159276745K.jpg", 
                                "pic/7552_116.4735,39.7841/09002200121707031815019251B.jpg", 
                                "pic/7552_116.4735,39.7841/09002200121707031815339421B.jpg", 
                                "pic/7552_116.4735,39.7841/09002200121707031817121071B.jpg", 
                                "pic/7552_116.4735,39.7841/09002200121707041511227541B.jpg", 
                                "pic/7552_116.4735,39.7841/09002200121707041515174721B.jpg"], 
                'poi_info': 'A peaceful **residential area** known for its lush **green spaces** and **parks**, this neighborhood is perfect for families and outdoor enthusiasts. The area offers tranquility away from the city’s hustle and bustle, yet it’s well-connected to central areas. 🌳🏡'},
    
    'Point 5': {'coords': [39.7809, 116.4905], 
                'remote_img': "pic/7605_116.4905,39.7809/7605.jpg", 
                'street_imgs': ["pic/7605_116.4905,39.7809/01002200001308171102407965K.jpg", 
                                "pic/7605_116.4905,39.7809/01002200001308181030509335K.jpg", 
                                "pic/7605_116.4905,39.7809/01002200001308181032249495K.jpg", 
                                "pic/7605_116.4905,39.7809/01002200001308181032424405K.jpg", 
                                "pic/7605_116.4905,39.7809/09002200121903101301333037M.jpg", 
                                "pic/7605_116.4905,39.7809/09002200122003161627083366G.jpg"], 
                'poi_info': 'Nestled between **historical sites** and **museums**, this district offers a glimpse into Beijing’s ancient past. It’s a popular destination for tourists interested in the city’s rich history and architecture. 🏛️📜'},
    
    'Point 6': {'coords': [39.7517, 116.1278], 
                'remote_img': "pic/7808_116.1278,39.7517/7808.jpg", 
                'street_imgs': ["pic/7808_116.1278,39.7517/01002200001308251545271375L.jpg"], 
                'poi_info': 'A suburban area on the outskirts of Beijing, this location is home to quiet **residential neighborhoods** and local **markets**. It offers a more relaxed pace of life while still providing access to the essentials of city living. 🏙️🏘️'},
    
    'Point 7': {'coords': [39.7307, 116.4013], 
                'remote_img': "pic/7868_116.4013,39.7307/7868.jpg", 
                'street_imgs': ["pic/7868_116.4013,39.7307/01002200001308311601397655T.jpg", 
                                "pic/7868_116.4013,39.7307/01002200001309011601260825T.jpg", 
                                "pic/7868_116.4013,39.7307/01002200001309011601396225T.jpg", 
                                "pic/7868_116.4013,39.7307/01002200001309011603330815T.jpg", 
                                "pic/7868_116.4013,39.7307/01002200001309011617380995T.jpg", 
                                "pic/7868_116.4013,39.7307/01002200001309011618200795T.jpg"], 
                'poi_info': 'This point is located near **industrial areas** and **technology hubs**, making it a growing location for businesses and tech startups. The area has seen rapid development in recent years, with plenty of modern infrastructure and opportunities. 🏢💼'},

    'Point 8': {'coords': [39.9133, 116.3691],
                'remote_img': "pic/6860_116.3691,39.9133_/6860.jpg",
                'street_imgs': ["pic/6860_116.3691,39.9133_/0100220000130810104132011J5.jpg",
                                "pic/6860_116.3691,39.9133_/0100220000130818092310143J5.jpg",
                                "pic/6860_116.3691,39.9133_/0900220000150525065106500T5.jpg",
                                "pic/6860_116.3691,39.9133_/09002200121902041435567412L.jpg"],
                'poi_info': 'This area is a bustling **commercial district** with a mix of **shopping centers**, **restaurants**, and **businesses**. It’s a popular spot for both locals and tourists looking for a vibrant urban experience. 🏬🍽️'},
    
    'Point 9': {'coords': [39.8904, 116.2777],
                'remote_img': "pic/6911_116.2777,39.8904_/6911.jpg",
                'street_imgs': ["pic/6911_116.2777,39.8904_/0100220000130724160835512J4.jpg",
                                "pic/6911_116.2777,39.8904_/09002200121706241459119509S.jpg",
                                "pic/6911_116.2777,39.8904_/09002200121706241459556769S.jpg",
                                "pic/6911_116.2777,39.8904_/09002200121902211249323977F.jpg"],
                'poi_info': 'This area is a vibrant **cultural district** with a mix of **art galleries**, **theaters**, and **historical sites**. It’s a hub for artists and creatives, offering a blend of traditional and contemporary cultural experiences. 🎭🖼️'},

    'Point 10': {'coords': [39.8792, 116.4981],
                'remote_img': "pic/6969_116.4981,39.8792_/6969.jpg",
                'street_imgs': ["pic/6969_116.4981,39.8792_/0100220000130730114135754J1.jpg",
                                "pic/6969_116.4981,39.8792_/0100220000130730121223847J1.jpg",
                                "pic/6969_116.4981,39.8792_/0100220000130730125921875J1.jpg",
                                "pic/6969_116.4981,39.8792_/0100220000130730125936048J1.jpg",
                                "pic/6969_116.4981,39.8792_/0100220000130730143201874J1.jpg"],
                'poi_info': 'This area is a lively **entertainment district** with a mix of **bars**, **clubs**, and **theaters**. It’s a popular nightlife spot for locals and visitors looking for fun and excitement. 🎶🍸'},

    'Point 11': {'coords': [39.8918, 116.4142],
                'remote_img': "pic/6967_116.4142,39.8918/6967.jpg",
                'street_imgs': ["pic/6967_116.4142,39.8918/0900220000150504023915158T5.jpg",
                                "pic/6967_116.4142,39.8918/0900220012200313100634661HG.jpg",
                                "pic/6967_116.4142,39.8918/09002200011507130509567265O.jpg",
                                "pic/6967_116.4142,39.8918/09002200011507130510277355O.jpg"],
                'poi_info': 'This area is a popular **shopping district** with a mix of **boutiques**, **malls**, and **markets**. It’s a great place to shop for fashion, accessories, and local souvenirs. 👗🛍️'},

    'Point 12': {'coords': [39.8856, 116.3527],
                'remote_img': "pic/7019_116.3527,39.8856/7019.jpg",
                'street_imgs': ["pic/7019_116.3527,39.8856/0900220000150502234151990T5.jpg",
                                "pic/7019_116.3527,39.8856/0900220000150503002105436T5.jpg",
                                "pic/7019_116.3527,39.8856/0900220000150503025712521T5.jpg",
                                "pic/7019_116.3527,39.8856/09002200011706181118100392Q.jpg",
                                "pic/7019_116.3527,39.8856/09002200011706181118233482Q.jpg"],
                'poi_info': 'This area is a charming **historical district** with a mix of **ancient temples**, **courtyards**, and **traditional teahouses**. It’s a peaceful spot to explore Beijing’s cultural heritage and enjoy a cup of tea. 🍵🏯'},

    'Point 13': {'coords': [39.8614, 116.3971],
                'remote_img': "pic/pic/7126_116.3971,39.8614/7126.jpg",
                'street_imgs': ["pic/7126_116.3971,39.8614/0900220000150503051825422O5.jpg",
                                "pic/7126_116.3971,39.8614/0900220000150507031652182O5.jpg",
                                "pic/7126_116.3971,39.8614/0900220000150507061212188O5.jpg",
                                "pic/7126_116.3971,39.8614/09002200122003151021409536G.jpg"],
                'poi_info': 'This area is a bustling **commercial hub** with a mix of **office buildings**, **shopping centers**, and **restaurants**. It’s a popular spot for business meetings, shopping, and dining out. 🏢🍽️'},

    'Point 14': {'coords': [39.8392, 116.3179],
                'remote_img': "pic/7230_116.3179,39.8392/7230.jpg",
                'street_imgs': ["pic/7230_116.3179,39.8392/0900220000150520023517991I6.jpg",
                                "pic/7230_116.3179,39.8392/0900220000150520031817058I6.jpg",
                                "pic/7230_116.3179,39.8392/0900220000150520040734073I6.jpg",
                                "pic/7230_116.3179,39.8392/01002200001309101439072695P.jpg",
                                "pic/7230_116.3179,39.8392/09002200011601101247373347O.jpg",
                                "pic/7230_116.3179,39.8392/09002200011601101249273657O.jpg"],
                'poi_info': 'This area is a vibrant **cultural district** with a mix of **art galleries**, **theaters**, and **historical sites**. It’s a hub for artists and creatives, offering a blend of traditional and contemporary cultural experiences. 🎭🖼️'}
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
        "餐馆": generate_random_pois(n=500),
        "娱乐": generate_random_pois(n=200),
        "文化": generate_random_pois(n=80)
    }

# 页面布局
st.title("🗺️ 探索北京 - 发现中国的中心！")
st.write("""
欢迎来到**北京**，中国繁华的首都，这里古老的文化与现代创新交相辉映！

在这里，您可以通过卫星视图、街景图像和关键兴趣点（POI）探索这座充满活力的城市的不同区域。无论是历史遗址、繁忙的集市，还是宁静的住宅区，北京的每个部分都讲述着独特的故事。让我们开启这段旅程吧！🌏✨
""")

# 添加带有表情符号的引导语句
st.markdown("""
### 如何探索地图？🧭
1. **浏览地图**：移动、放大或缩小，探索北京的不同区域。
2. **点击标记点**：选择一个标记点，了解该区域的更多信息，从卫星视图到街景视角。
3. **查看详情**：点击标记点后，该区域的信息将显示在右侧。您将看到卫星视图、街景照片以及当地热点或历史地标。

🔍 **提示**：想了解北京的中心地带或探索隐藏的宝藏吗？只需点击任意标记点，让这座城市的魅力展现出来！
""")

# 添加关于北京文化和地标的简短介绍
st.write("""
### 一瞥北京的魔力 🏛️
北京不仅是中国的政治中心，它还是拥有丰富历史地标的城市，如**故宫**、**天安门广场**和**颐和园**。
除此之外，城市中还遍布着传统的胡同、现代的摩天大楼以及文化遗产，形成了新旧交融的迷人景象。
城市的每个角落都有其特别之处，无论是熙熙攘攘的集市、宁静的公园，还是安静的居民小巷。

现在，让我们探索北京的多样化区域吧！🌆
""")

# 创建包含两列的布局
col1, col2 = st.columns([2, 1])

# 左列：显示地图
with col1:
    # 初始化地图，中心点为北京
    m = folium.Map(location=[39.9042, 116.4074], zoom_start=11)

    # 添加预定义点的标记
    add_markers_to_map(m, beijing_points)
    # 添加会话状态中的自定义点
    for custom_point in st.session_state.custom_points:
        folium.Marker(location=custom_point, popup="自定义点", icon=folium.Icon(color='red')).add_to(m)

    # 为每个点添加标记
    for point_name, point_info in beijing_points.items():
        folium.Marker(location=point_info['coords'], popup=point_name).add_to(m)

    # 用户添加点功能
    user_lat = st.number_input("输入纬度：", min_value=39.0, max_value=41.0, value=39.9)
    user_lng = st.number_input("输入经度：", min_value=115.0, max_value=117.0, value=116.4)
    
    if st.button("添加自定义点"):
        # 将自定义点添加到会话状态中
        st.session_state.custom_points.append([user_lat, user_lng])
        st.success(f"已添加点 ({user_lat}, {user_lng})")

    # 添加兴趣点类别过滤器
    poi_filter = st.selectbox("筛选兴趣点类别：", ["无", "餐馆", "娱乐", "文化"])
    
    # 根据选择的类别添加100个随机兴趣点的热力图
    if poi_filter != "无":
        poi_points = st.session_state.poi_categories[poi_filter]
        heatmap = HeatMap(poi_points, radius=15, blur=10)
        heatmap.add_to(m)

    # 显示地图
    map_data = st_folium(m, width=700, height=700)

# 右列：显示点击点的详细信息
with col2:
    st.write("### 深入了解该区域 🎯")
    
    # 当点击标记点时显示数据
    if map_data['last_object_clicked']:
        clicked_coords = map_data['last_object_clicked']['lat'], map_data['last_object_clicked']['lng']
        
        # 查找并显示点击点的信息
        for point_name, point_info in beijing_points.items():
            if clicked_coords == tuple(point_info['coords']):
                st.subheader(f"探索 {point_name} 🌟")
                
                # 首先显示兴趣点信息
                st.write(f"**兴趣点**: {point_info['poi_info']} 🏙️")
                
                # 显示同尺寸的遥感图像和街景图像
                st.write("**遥感图像 🛰️:**")
                st.image(point_info['remote_img'], caption="卫星图像", use_column_width=True)

                st.write("**街景图 🚶:**")
                # 检查是否有多张街景图片
                if len(point_info['street_imgs']) > 1:
                    # 如果有多张图像，则使用滑块浏览
                    street_img_idx = st.slider("街景图像索引", 0, len(point_info['street_imgs']) - 1, 0)
                    st.image(point_info['street_imgs'][street_img_idx], caption="街景图像", use_column_width=True)
                else:
                    # 如果只有一张图像，直接显示
                    st.image(point_info['street_imgs'][0], caption="街景图像", use_column_width=True)

    else:
        st.write("点击标记点以查看该区域的详细信息 ⬅️。")

# 添加页脚或最后的消息
st.write("""
#### 准备好揭开更多的秘密了吗？🧳
无论您是历史爱好者、城市探险家，还是只是好奇，北京总有一份惊喜等待着您！ 
继续探索地图，点击不同的点，沉浸在这座迷人城市的不同层次中吧。
""")
