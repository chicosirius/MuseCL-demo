import streamlit as st
import pandas as pd
import json

# 设置页面配置
st.set_page_config(page_icon="🌍", layout="wide")

# 自定义侧边栏
markdown = """
*MuseCL: 通过多语义对比学习预测城市社会经济指标。*

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

st.write("""
# MuseCL - IJCAI2024

这是我们在 IJCAI2024 的 Social Good Track 论文的演示实现：*MuseCL: 通过多语义对比学习预测城市社会经济指标*。

## 概述

""")

# 使用 st.image 显示图片
st.image("pic/framework.jpg", caption="框架概述", use_column_width=True)

st.write("""
该多步对比学习模型由**三个关键组件组成：从视觉模态中提取语义特征、结合文本语义信息以及执行下游任务。**
首先，我们将视觉语义学习模块划分为基于 POI 相似性的遥感图像表示和基于人口流动相似性的街景图像表示。精心挑选对比学习样本对，以获取具有不同关注点的图像特征。随后，我们考虑与每个区域相关的 POI 文本信息，并利用预训练的编码器模型为每个区域提取文本特征。然后，使用特征级注意力融合模块，我们将结合的遥感和街景特征与每个区域的文本表示向量对齐，从而为融合特征注入视觉和文本的语义信息。最后，我们在一系列下游任务中评估每个区域的低维表示。

## 数据集详细信息

#### 区域划分

在表示区域之前，划分最小单元是必要的。常见的方法包括不规则的道路网络、方形网格和六边形网格。

(a) 中的道路网络分割使用城市交通网络将城市划分为大小和形状各异的区域。缺点是形状复杂，难以处理多模态数据，且缺乏标准化表示。在实际中，常见的方法是基于规则形状的划分。图 (b) 中的划分采用基于方形的方法，将城市划分为均匀的方块。该方法适用于地形和道路布局规则的城市区域，但缺乏变化。

为了结合道路网络和方形划分的优势，六边形划分成为一种灵活且创新的选择。在六边形划分中，区域呈错列分布，可以邻接六个区域，从而更好地体现相关性。这种方法能够适应不规则的道路网络和地形，带来更丰富的城市空间配置。因此，我们选择六边形划分来划分城市表示单元，如图 (c) 所示。

""")

# 使用 st.image 显示图片
st.image("pic/region_split.jpg", caption="区域划分概述", use_column_width=True)

st.write("""
#### 城市多模态数据

根据框架，数据收集包括获取街景图像、遥感图像、POI 数据和人口流动数据。

- **街景图像。** 可以通过百度地图和谷歌地图 API 获取。可以使用 ArcGIS 沿着道路网络选择图像采样位置，并获得一定数量的全景图像。最终，每张图像被分为四个部分：0° - 90°，90° - 180°，180° - 270°，270° - 360°。

- **遥感图像。** 可以通过 Google Earth 的卫星图像接口获取。这些图像可以被裁剪成单独的最小表示单元，并根据不同城市的具体区域划分调整其大小。

- **POI 数据。** 它通过百度地图和 OpenStreetMap (OSM) 收集，包括时间、评分、评论内容和位置等。不完整的数据将被排除。最终的数据集保留了 POI 名称、评论内容、POI 标签以及经纬度坐标。

- **人口流动。** 我们使用出租车在特定时间段内的出行模式来近似每个区域的人口流动情况。例如，在北京，我们使用 2008 年 2 月 2 日至 2008 年 8 月 2 日期间 10,357 辆出租车的每周轨迹，数据集包含 1500 万个点，轨迹总距离为 900 万公里。

在数据收集和预处理后，三个城市的数据集总结如下表所示。
""")

# 使用 st.image 显示图片
st.image("pic/dataset_statistics.jpg", caption="数据集统计", use_column_width=True)

st.write("""
#### 社会经济指标

为了全面展示我们模型在多种城市属性上的预测能力，选择了一系列区域特征进行实验。数据来源及其链接如下所示。

- **人口密度。** 北京 & 上海 & 纽约：WorldPop，https://www.worldpop.org/。
- **住房密度。** 北京 & 上海：链家，https://m.lianjia.com/。
- **POI/评论数量。** 北京 & 上海：百度地图 API，http://api.map.baidu.com。纽约：OpenStreetMap，https://www.openstreetmap.org/。
- **人口流动。** 北京：微软研究院，https://www.microsoft.com/en-us/research/。上海：香港科技大学，https://cse.hkust.edu.hk/scrg/。纽约：Kaggle，https://www.kaggle.com/datasets。
- **犯罪数据。** 纽约：NYC Open Data，https://opendata.cityofnewyork.us/。
""")


st.write("""
## 结果
""")

# 使用 st.image 显示图片
st.image("pic/result1.jpg", caption="结果 1", use_column_width=True)
st.image("pic/result2.jpg", caption="结果 2", use_column_width=True)
