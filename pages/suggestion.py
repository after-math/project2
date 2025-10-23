import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np

# ========== 页面配置 ==========
st.set_page_config(page_title="优化建议", page_icon="💡", layout="wide")

# ========== 全局样式优化 ==========
st.markdown("""
<style>
/* 主容器边距 */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* 字体修复：防止 emoji 高度错位 */
h1, h2, h3, p, span {
    font-family: "PingFang SC", "Microsoft YaHei", "Arial", sans-serif !important;
    line-height: 1.5em;
}

/* 分区容器 */
.section {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 20px 25px;
    margin-bottom: 25px;
}

/* 右侧配置框 */
.right-box {
    background-color: #eef3fa;
    border-radius: 12px;
    padding: 20px;
    height: 100%;
}

/* 次级卡片 */
.subcard {
    background-color: #faeaea;
    border-radius: 12px;
    padding: 18px;
    margin-top: 12px;
}

/* 全宽块：避免vw导致溢出 */
.full-width {
    width: 100%;
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 25px 30px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ========== 页面标题 ==========
col_title, col_space = st.columns([5, 1])
with col_title:
    st.markdown("## 💡 优化建议")

# ========== 左右主布局 ==========
main_col, side_col = st.columns([3.2, 1.1], gap="large")

# ========== 左侧主体内容 ==========
with main_col:
    # --- 1️⃣ 优化前后时段对比 ---
    with st.container():
        st.markdown("### ⏱️ 优化前后时段对比")

        option = {
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["原用电时段", "优化后推荐时段"], "top": 10},
            "grid": {"left": "5%", "right": "5%", "bottom": "10%", "containLabel": True},
            "xAxis": {"type": "value", "name": "时间（小时）"},
            "yAxis": {"type": "category", "data": ["电热水器", "洗碗机", "洗碗机1", "微波炉"]},
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

# ========== 右侧侧边栏 ==========
with side_col:
    st.markdown('<div class="right-box">', unsafe_allow_html=True)
    st.markdown("#### ⚙️ 权重设置")

    w1 = st.number_input("电费权重", 0.0, 1.0, 0.7, 0.1)
    w2 = st.number_input("舒适度权重", 0.0, 1.0, 0.3, 0.1)

    st.caption("提示：电费权重越高越节能，舒适权重越高则更注重体验。")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 2️⃣ 优化前后目标对比 ==========
st.markdown('<div class="full-width">', unsafe_allow_html=True)
st.markdown("### 📊 优化前后目标对比")

device = st.selectbox("请选择要查看的电器", ["微波炉", "电热水器", "洗碗机"])
st.markdown('<div class="subcard">', unsafe_allow_html=True)

# --- 三列数据展示 ---
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**昨日用电时段**")
    st.write("07:21–08:05\n18:09–19:10")
with c2:
    st.markdown("**建议用电时段**")
    st.write("06:18–07:30\n17:15–18:40")
with c3:
    st.markdown("**电费 (¥)**")
    st.metric("优化前", "9.10")
    st.metric("优化后", "8.13")

# --- 两列说明 ---
c4, c5 = st.columns(2)
with c4:
    st.markdown("**前后舒适度变化**")
    st.write("前：1.0000\n后：0.9375")
with c5:
    st.markdown("**说明**")
    st.write("优化后整体舒适度略降，但节约约10.6%电费。")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
