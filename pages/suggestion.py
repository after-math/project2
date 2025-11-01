import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np

# ========== 页面配置 ==========
st.set_page_config(page_title="优化建议", page_icon="💡", layout="centered")

# ========== 全局样式优化 ==========
st.markdown("""
<style>

/* ======================== */
/* 🌐 主容器边距设置（控制页面整体上下间距） */
/* ======================== */
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}

/* ======================== */
/* 📝 全局字体样式 */
/* ======================== */
# h1, h2, h3, p, span, div {
#     font-family: "PingFang SC", "Microsoft YaHei", "Arial", sans-serif !important;
#     line-height: 1.6em;
# }

/* ======================== */
/* 🧩 区域模块容器 */
/* ======================== */
.section {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 25px 30px;
    margin-bottom: 25px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}

/* ======================== */
/* ⚙️ 右侧配置框 */
/* ======================== */
.right-box {
    background-color: #eef3fa;
    border-radius: 12px;
    padding: 25px;
    height: 100%;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* ======================== */
/* 📊 子卡片区块 */
/* ======================== */
.subcard {
    background-color: #ffffff;
    border: 1px solid #e3e6ec;
    border-radius: 12px;
    padding: 25px 30px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-top: 10px;
}

/* ======================== */
/* 📈 底部对比模块 */
/* ======================== */
.full-width {
    width: 100%;
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 25px 30px;
    margin-top: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ======================== */
/* 💡 标题样式统一 */
/* ======================== */
h2, h3, h4 {
    color: #2a3f5f;
    font-weight: 600;
}

/* ======================== */
/* 🪞 分割线美化 */
/* ======================== */
hr {
    border: none;
    border-top: 1px solid #eee;
    margin: 20px 0;
}

/* ======================== */
/* ✨ 优化交互按钮 */
/* ======================== */
div.stButton > button {
    background-color: #4C9AFF;
    color: white;
    border-radius: 8px;
    border: none;
    height: 2.5em;
    font-weight: 500;
    transition: 0.2s;
}
div.stButton > button:hover {
    background-color: #0078D7;
}
</style>
""", unsafe_allow_html=True)

# ========== 页面标题 ==========
st.markdown("## 💡 优化建议")
st.markdown('<div class="section">', unsafe_allow_html=True)

# 不再需要右侧栏，只保留主列
main_col, _ = st.columns([4, 0.0001])  # 第二列宽度近乎为0

# ========== 主体内容 ==========
with main_col:

    # ---------- 权重设置（横向放在图上方） ----------
    st.markdown("#### ⚙️ 权重设置")
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        w1 = st.number_input("电费权重", 0.0, 1.0, 0.7, 0.1, key="w1")
    with col2:
        w2 = st.number_input("舒适度权重", 0.0, 1.0, 0.3, 0.1, key="w2")

    st.caption("💬 电费权重越高越节能，舒适度权重越高则更注重使用体验。")

    st.markdown("### ⏱️ 优化前后时段对比（多时段展示）")

# ========= 数据 =========
devices = ["电热水器", "洗衣机", "洗碗机", "微波炉"]

before = [
    [(6.5, 8.0), (18.0, 20.0)],
    [(8.0, 9.0), (20.0, 21.0)],
    [(9.0, 10.0), (19.0, 20.0)],
    [(7.0, 8.0), (21.0, 22.0)],
]
after = [
    [(6.0, 7.5), (17.5, 19.0)],
    [(7.5, 8.5), (19.5, 20.5)],
    [(8.5, 9.5), (18.5, 19.5)],
    [(6.5, 7.5), (20.0, 21.0)],
]

# ========= 构造甘特条数据 =========
def build_bar_data(time_ranges, color):
    bars = []
    for i, dev in enumerate(devices[::-1]):  # 倒序画
        for start, end in time_ranges[i]:
            bars.append({
                "value": [start, end - start, dev],
                "itemStyle": {"color": color},
                "label": {"show": False}
            })
    return bars

# ========= ECharts 配置 =========
option = {
    "tooltip": {
        "trigger": "item",
        # ✅ 用 JS 字符串实现 formatter
        "formatter": """
            function (params) {
                var s = params.value;
                var start = s[0];
                var end = s[0] + s[1];
                return s[2] + '<br/>' + start.toFixed(2) + '–' + end.toFixed(2) + ' 小时';
            }
        """
    },
    "legend": {"data": ["原用电时段", "优化后用电时段"], "top": 10},
    "grid": {"left": "10%", "right": "5%", "bottom": "10%", "containLabel": True},
    "xAxis": {
        "type": "value",
        "min": 0,
        "max": 24,
        "name": "时间（小时）",
        "axisLabel": {"formatter": "{value}:00"},
        "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.3}},
    },
    "yAxis": {
        "type": "category",
        "data": devices[::-1],
        "axisLabel": {"fontSize": 13, "margin": 12},
    },
    "series": [
        {
            "name": "原用电时段",
            "type": "bar",
            "barWidth": 14,
            "encode": {"x": [0, 1], "y": 2},
            "data": build_bar_data(before, "#4a6ee0"),
        },
        {
            "name": "优化后用电时段",
            "type": "bar",
            "barWidth": 14,
            "encode": {"x": [0, 1], "y": 2},
            "data": build_bar_data(after, "#f6a23c"),
        },
    ]
}

st_echarts(option, height="500px")

# ========== 2️⃣ 优化前后目标对比 ==========
# st.markdown('<div class="full-width">', unsafe_allow_html=True)
st.markdown("### 📊 优化前后目标对比")
st.markdown("<div style='font-size:18px; font-weight:500;'>请选择要查看的电器</div>", unsafe_allow_html=True)

device = st.selectbox("", ["微波炉", "电热水器", "洗碗机"])

# st.markdown('<div class="subcard">', unsafe_allow_html=True)


# ======== 表格样式 ========
st.markdown("""
<style>
.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'PingFang SC', 'Microsoft YaHei';
    margin-bottom: 10px;
}

.custom-table th, .custom-table td {
    border: 1px solid #e0e0e0;
    text-align: center;
    padding: 10px;
    font-size: 15px;
}

.custom-table th {
    background-color: #f5f7fa;
    font-weight: 600;
}

.custom-table caption {
    caption-side: top;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 6px;
}

.highlight {
    background-color: #e8f4ff;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ======== 表格主体 ========
st.markdown("""
<table class="custom-table">
    <caption>⚡ 用电优化对比</caption>
    <thead>
        <tr>
            <th>昨日用电时段</th>
            <th>建议用电时段</th>
            <th>电费 (¥)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>07:21–08:05<br>18:09–19:10</td>
            <td>06:18–07:30<br>17:15–18:40</td>
            <td>
                <span class="highlight">优化前：9.10</span><br>
                <span class="highlight">优化后：8.13</span>
            </td>
        </tr>
    </tbody>
</table>

<table class="custom-table">
    <thead>
        <tr>
            <th>前后舒适度变化</th>
            <th>说明</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>前：1.0000<br>后：0.9375</td>
            <td>优化后整体舒适度略降，但节约约 10.6% 电费。</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# 关闭 subcard 与 full-width div
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
