import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np

# ========== 页面配置 ==========
st.set_page_config(page_title="优化建议", page_icon="💡", layout="centered")
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
<style>
/* 保证移动端字体与桌面一致 */
html, body {
    zoom: 1.0 !important;
    -webkit-text-size-adjust: 100% !important;
}

/* 让 Streamlit 主内容区在移动端不缩小 */
[data-testid="stAppViewContainer"] {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* 调整标题在手机端的比例 */
@media (max-width: 768px) {
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.2rem !important; }
    p, span, div { font-size: 1rem !important; }
    [data-testid="stSidebar"] { width: 80vw !important; }
}
</style>
""", unsafe_allow_html=True)
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

# ========== 左右主布局 ==========
main_col, side_col = st.columns([3.2, 1.1], gap="large")

# ========== 左侧主体内容 ==========
with main_col:
    st.markdown("### ⏱️ 优化前后时段对比")

    option = {
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["原用电时段", "优化后推荐时段"], "top": 10},
        "grid": {"left": "5%", "right": "5%", "bottom": "10%", "containLabel": True},
        "xAxis": {"type": "value", "name": "时间（小时）"},
        "yAxis": {"type": "category", "data": ["电热水器", "洗碗机", "洗衣机", "微波炉"]},
        "series": [
            {
                "name": "原用电时段",
                "type": "bar",
                "data": [8, 12, 15, 18],
                "itemStyle": {"color": "#4C9AFF"},
            },
            {
                "name": "优化后推荐时段",
                "type": "bar",
                "data": [6, 10, 13, 17],
                "itemStyle": {"color": "#F5A623"},
            },
        ],
    }
    st_echarts(option, height="350px", key="bar")

# ========== 右侧配置栏 ==========
with side_col:
    st.markdown('<div class="right-box">', unsafe_allow_html=True)
    st.markdown("#### ⚙️ 权重设置")
    w1 = st.number_input("电费权重", 0.0, 1.0, 0.7, 0.1)
    w2 = st.number_input("舒适度权重", 0.0, 1.0, 0.3, 0.1)
    st.caption("💬 提示：电费权重越高越节能，舒适度权重越高则更注重使用体验。")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 2️⃣ 优化前后目标对比 ==========
st.markdown('<div class="full-width">', unsafe_allow_html=True)
st.markdown("### 📊 优化前后目标对比")
st.markdown("<div style='font-size:18px; font-weight:500;'>请选择要查看的电器</div>", unsafe_allow_html=True)

device = st.selectbox("", ["微波炉", "电热水器", "洗碗机"])

st.markdown('<div class="subcard">', unsafe_allow_html=True)

# 第一行三列（对比信息）
c1, c2, c3 = st.columns([1.2, 1.2, 1])

with c1:
    st.markdown('<p>昨日用电时段</p>', unsafe_allow_html=True)
    st.write("07:21–08:05  \n18:09–19:10")

with c2:
    st.markdown('<p>建议用电时段</p>', unsafe_allow_html=True)
    st.write("06:18–07:30  \n17:15–18:40")

with c3:
    st.markdown('<p>电费 (¥)</p>', unsafe_allow_html=True)
    st.metric("优化前", "9.10")
    st.metric("优化后", "8.13")

st.markdown("<hr>", unsafe_allow_html=True)

# 第二行两列（说明部分）
c4, c5 = st.columns([1, 1.5])
with c4:
    st.markdown('<p>前后舒适度变化</p>', unsafe_allow_html=True)
    st.write("前：1.0000  \n后：0.9375")

with c5:
    st.markdown('<p>说明</p>', unsafe_allow_html=True)
    st.write("优化后整体舒适度略降，但节约约 10.6% 电费。")

# 关闭 subcard 与 full-width div
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
