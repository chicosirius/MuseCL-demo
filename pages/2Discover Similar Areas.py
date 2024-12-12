import time
import streamlit as st
import pandas as pd
import pydeck as pdk

# 设置页面配置
st.set_page_config(page_title="探索相似地区", page_icon="🌍", layout="wide")

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

# 初始化 session_state
if 'data_uploaded' not in st.session_state:
    st.session_state['data_uploaded'] = False
if 'clicked_area' not in st.session_state:
    st.session_state['clicked_area'] = None
if 'similarity_calculated' not in st.session_state:
    st.session_state['similarity_calculated'] = False

# 标题和简介
st.title("🔍 发现相似的城市区域")
st.markdown("""
欢迎来到 **终极城市探索者**！🌆✨  
是否曾经想过，不同城市区域在社会经济方面是如何相互比较的？让我们深入探索跨城市的相似性检测。选择 **北京的内置数据** 或上传您自己城市的数据，看看哪些区域最接近匹配。

**准备好探索了吗？让我们开始吧！**
""")

# 上传数据选项
st.subheader("选择您的数据源 📊")
data_selection = st.selectbox(
    "您想使用自己的数据集，还是探索北京的现有数据？",
    ("无", "上传我自己的数据", "使用内置的北京数据")
)

# 用户上传自定义数据
if data_selection == "上传我自己的数据" and not st.session_state['data_uploaded']:
    st.session_state['similarity_calculated'] = False

    st.write("🎒 准备好您的数据之旅！请上传所有区域的以下数据文件：")
    street_images = st.file_uploader("📷 上传街景图片", type=['png', 'jpg', 'jpeg', 'zip'], accept_multiple_files=True)
    remote_images = st.file_uploader("🛰️ 上传遥感图像", type=['tif', 'png', 'jpg', 'zip'], accept_multiple_files=True)
    poi_data = st.file_uploader("📌 上传POI数据（CSV）", type=['csv'])
    population_data = st.file_uploader("👥 上传人口流动数据（CSV）", type=['csv'])

    if street_images and remote_images and poi_data and population_data:
        st.success("所有文件上传完成！您已准备好开始计算相似性。")
        st.session_state['data_uploaded'] = True
elif data_selection == "使用内置的北京数据":
    st.success("使用内置的北京数据！您已准备好开始计算相似性。")
elif data_selection == '无':
    st.warning("🚫 请选择一个数据源以开始探索。")


# 开始计算按钮
# 开始计算按钮
if st.session_state['data_uploaded'] or data_selection == "使用内置的北京数据":
    if st.button("开始相似度计算") or st.session_state['similarity_calculated']:

        with st.spinner("请稍等片刻，我们正在计算相似度... 🚀"):
            time.sleep(1)

        st.session_state['similarity_calculated'] = True  # 设置按钮状态为已计算

        # 模拟的区域数据
        areas = [
            {"name": "朝阳区点1", "lat": 39.9219, "lon": 116.4433, "similar": "丰台区点5"},
            {"name": "海淀区点2", "lat": 39.9997, "lon": 116.3267, "similar": "西城区点4"},
            {"name": "东城区点3", "lat": 39.9309, "lon": 116.4167, "similar": "海淀区点2"},
            {"name": "西城区点4", "lat": 39.9123, "lon": 116.3661, "similar": "东城区点3"},
            {"name": "丰台区点5", "lat": 39.8586, "lon": 116.2869, "similar": "朝阳区点1"}
        ]

        others = [ 
            {"name": "石景山区点", "lat": 39.9145, "lon": 116.1956},
            {"name": "通州区点", "lat": 39.9026, "lon": 116.6633},
            {"name": "昌平区点", "lat": 40.2208, "lon": 116.2334},
            {"name": "大兴区点", "lat": 39.7181, "lon": 116.4053},
            {"name": "房山区点", "lat": 39.7025, "lon": 115.9928},
            {"name": "门头沟区点", "lat": 39.9384, "lon": 116.1061},
            {"name": "平谷区点", "lat": 40.1448, "lon": 117.1001},
            {"name": "怀柔区点", "lat": 40.3344, "lon": 116.6377},
            {"name": "密云区点", "lat": 40.3774, "lon": 116.8414},
            {"name": "海淀区点", "lat": 39.9997, "lon": 116.3267},
            {"name": "顺义区点", "lat": 40.1276, "lon": 116.6558},
            {"name": "延庆区点", "lat": 40.4653, "lon": 115.9854},
            {"name": "昌平区点", "lat": 40.2208, "lon": 116.2334},
            {"name": "大兴区点", "lat": 39.7181, "lon": 116.4053},
            {"name": "房山区点", "lat": 39.7025, "lon": 115.9928},
            {"name": "门头沟区点", "lat": 39.9384, "lon": 116.1061},
            {"name": "平谷区点", "lat": 40.1448, "lon": 117.1001},
            {"name": "怀柔区点", "lat": 40.3344, "lon": 116.6377},
            {"name": "密云区点", "lat": 40.3774, "lon": 116.8414},
            {"name": "海淀区点", "lat": 39.9997, "lon": 116.3267},
            {"name": "顺义区点", "lat": 40.1276, "lon": 116.6558},
            {"name": "延庆区点", "lat": 40.4653, "lon": 115.9854},
            {"name": "朝阳区点", "lat": 39.9219, "lon": 116.4433},
            {"name": "亦庄区点", "lat": 39.7955, "lon": 116.5065}
        ]


        # 模拟生成每个区域的POI信息、遥感图像和街景图像
        sample_data = {
            "朝阳区点1": {
                "poi": "朝阳公园 🌳, 中央电视台总部大楼 📺",
                "remote_sensing": "pic/6969_116.4981,39.8792_/6969.jpg",
                "street_views": [
                    "pic/6969_116.4981,39.8792_/0100220000130730143201874J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730114135754J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730121223847J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730125921875J1.jpg",
                    "pic/6969_116.4981,39.8792_/0100220000130730125936048J1.jpg"
                ]
            },
            "海淀区点2": {
                "poi": "中关村科技园 💻, 北京大学 🎓",
                "remote_sensing": "pic/6859_116.3372,39.9092_/6859.jpg",
                "street_views": [
                    "pic/6859_116.3372,39.9092_/0900220000150520053741088A6.jpg",
                    "pic/6859_116.3372,39.9092_/01002200001309261617204985L.jpg",
                    "pic/6859_116.3372,39.9092_/09002200121902071504097782L.jpg",
                    "pic/6859_116.3372,39.9092_/09002200121902071504197972L.jpg",
                    "pic/6859_116.3372,39.9092_/09002200122003121235474337C.jpg"
                ]
            },
            "东城区点3": {
                "poi": "天安门广场 🏯, 王府井大街 🛍️",
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
            "西城区点4": {
                "poi": "北海公园 🌊, 国家大剧院 🎭",
                "remote_sensing": "pic/6860_116.3691,39.9133_/6860.jpg",
                "street_views": [
                    "pic/6860_116.3691,39.9133_/0100220000130810104132011J5.jpg",
                    "pic/6860_116.3691,39.9133_/0100220000130818092310143J5.jpg",
                    "pic/6860_116.3691,39.9133_/0900220000150525065106500T5.jpg",
                    "pic/6860_116.3691,39.9133_/09002200121902041435567412L.jpg"
                ]
            },
            "丰台区点5": {
                "poi": "北京园博园 🌸, 卢沟桥 🏰",
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
        st.markdown("点击任意区域标记以查看其详细信息和最相似的地区！🎯")

        # 显示区域选择框
        clicked_area = st.selectbox("手动选择一个区域（如果点击无效）:", options=["无"] + [area["name"] for area in areas], index=0)

        # 只有当用户选择了区域时才显示详细信息和最相似区域
        if clicked_area != "无":
            st.session_state['clicked_area'] = clicked_area  # 保存用户选择的区域
            similar_area = next(area["similar"] for area in areas if area["name"] == clicked_area)
            st.subheader(f"{clicked_area} 的详细信息及其最相似的区域: {similar_area}")

            # 使用 columns 进行左右对比显示
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {clicked_area}")
                st.markdown(f"**兴趣点数据**: {sample_data[clicked_area]['poi']}")
                st.markdown(f"**遥感图像**:")
                st.image(sample_data[clicked_area]['remote_sensing'], caption=f"{clicked_area} 的遥感图像")
                st.markdown(f"**街景**:")
                if len(sample_data[clicked_area]['street_views']) > 1:
                    # 如果有多张街景图片，使用滑块浏览
                    street_img_idx = st.slider("街景图片索引", 0, len(sample_data[clicked_area]['street_views']) - 1, 0, key=f"street_view_slider_{clicked_area}")
                    st.image(sample_data[clicked_area]['street_views'][street_img_idx], caption="街景")
                else:
                    st.image(sample_data[clicked_area]['street_views'][0], caption=f"{clicked_area} 的街景 1")

            with col2:
                st.markdown(f"### {similar_area}")
                st.markdown(f"**兴趣点数据**: {sample_data[similar_area]['poi']}")
                st.markdown(f"**遥感图像**:")
                st.image(sample_data[similar_area]['remote_sensing'], caption=f"{similar_area} 的遥感图像")
                st.markdown(f"**街景**:")
                if len(sample_data[similar_area]['street_views']) > 1:
                    # 如果有多张街景图片，使用滑块浏览
                    street_img_idx = st.slider("街景图片索引", 0, len(sample_data[similar_area]['street_views']) - 1, 0, key=f"street_view_slider_{similar_area}")
                    st.image(sample_data[similar_area]['street_views'][street_img_idx], caption="街景")
                else:
                    st.image(sample_data[similar_area]['street_views'][0], caption=f"{similar_area} 的街景 1")

# 页脚
st.markdown("---")
st.markdown("""
本工具使用我们的先进 **MuseCL 模型** 分析城市数据，为您带来之前可能未曾注意到的见解。🎯  
敬请期待更多更新和激动人心的新功能！
""")
