import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np

# ========== 页面配置 ==========
st.set_page_config(page_title="优化建议", page_icon="💡", layout="wide")

# ========== 全局样式优化 ==========
st.markdown("""
<style>

/* ======================== */
/* 🌐 主容器边距设置（控制页面整体上下间距） */
/* ======================== */
.block-container {
    padding-top: 2rem;     /* 页面顶部内边距：让内容不要紧贴浏览器上沿 */
    padding-bottom: 1rem;  /* 页面底部内边距：让内容不要太靠下 */
}

/* ======================== */
/* 📝 全局字体样式（修复emoji错位 + 统一字体） */
/* ======================== */
h1, h2, h3, p, span {
    font-family: "PingFang SC", "Microsoft YaHei", "Arial", sans-serif !important;
    /* 优先使用苹方（macOS）或微软雅黑（Windows），都没有就用 Arial */
    line-height: 1.5em;   /* 设置行距为字体高度的1.5倍，使文本更易读 */
}

/* ======================== */
/* 🧩 分区容器（用于包裹每一段主要内容） */
/* ======================== */
.section {
    background-color: #f9f9f9;  /* 浅灰色背景，区分不同区域 */
    border-radius: 12px;        /* 圆角边框，美观柔和 */
    padding: 20px 25px;         /* 内边距，上下20px、左右25px，保证内容不贴边 */
    margin-bottom: 25px;        /* 与下一个区域的间距 */
}

/* ======================== */
/* ⚙️ 右侧配置框（比如权重设置栏） */
/* ======================== */
.right-box {
    background-color: #eef3fa;  /* 淡蓝色背景，突出右侧区域 */
    border-radius: 12px;        /* 圆角边框 */
    padding: 20px;              /* 内边距：四周留空 */
    height: 100%;               /* 高度占满所在列 */
}

/* ======================== */
/* 🧾 次级卡片（用于小模块、子信息） */
/* ======================== */
.subcard {
    background-color: #faeaea;  /* 浅红色背景，用来区分次要信息块 */
    border-radius: 12px;        /* 圆角边框 */
    padding: 18px;              /* 内边距 */
    margin-top: 12px;           /* 与上一个元素的垂直间距 */
}

/* ======================== */
/* 📊 全宽块（用于底部对比图、汇总模块） */
/* ======================== */
.full-width {
    width: 100%;                /* 占满整行宽度 */
    background-color: #f9f9f9;  /* 浅灰背景，与.section 保持一致 */
    border-radius: 12px;        /* 圆角边框 */
    padding: 25px 30px;         /* 内边距更大，适合大内容展示 */
    margin-top: 20px;           /* 与上方内容留出空隙 */
}
/* 卡片整体容器 */
.subcard {
    background-color: #ffffff;     /* 白底 */
    border: 1px solid #e3e6ec;     /* 淡灰边框 */
    border-radius: 12px;           /* 圆角 */
    padding: 25px 30px;            /* 内边距 */
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);  /* 轻阴影 */
    margin-top: 10px;
}

/* 标题 */
h4 {
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    color: #2a3f5f;
    margin-bottom: 8px;
}

/* 指标标题 */
.metric-label {
    font-weight: bold;
    color: #2a3f5f;
    margin-bottom: 6px;
}

/* 分割线 */
hr {
    border: none;
    border-top: 1px solid #eee;
    margin: 15px 0;
}

/* 调整列间距 */
[data-testid="stHorizontalBlock"] {
    gap: 2rem !important;
}
</style>

""", unsafe_allow_html=True)

# ========== 页面标题 ==========
col_title, col_space = st.columns([5, 1])
with col_title:
    st.markdown("## 💡 优化建议")
st.markdown('<div class="section">',unsafe_allow_html=True)

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
    # st.markdown('<div class="right-box">', unsafe_allow_html=True)
    st.markdown("#### ⚙️ 权重设置")
    st.markdown('<div style="padding:30px">', unsafe_allow_html=True)
    w1 = st.number_input("电费权重", 0.0, 1.0, 0.7, 0.1)
    st.markdown('<div style="padding:20px">', unsafe_allow_html=True)
    w2 = st.number_input("舒适度权重", 0.0, 1.0, 0.3, 0.1)
    st.markdown('<div style="padding:10px">', unsafe_allow_html=True)
    st.caption("提示：电费权重越高越节能，舒适权重越高则更注重体验。")
    st.markdown('</div class="right-box">', unsafe_allow_html=True)

# ========== 2️⃣ 优化前后目标对比 ==========
st.markdown('<div class="full-width">', unsafe_allow_html=True)
st.markdown("### 📊 优化前后目标对比")
st.markdown("<div style='font-size:20px'>请选择要查看的电器</div>",unsafe_allow_html=True)
device = st.selectbox("", ["微波炉", "电热水器", "洗碗机"])
st.markdown('<div class="subcard">', unsafe_allow_html=True)

# st.markdown('<div class="subcard">', unsafe_allow_html=True)

# 第一行三列（对比）
c1, c2, c3 = st.columns([1.2, 1.2, 1])

with c1:
    st.markdown('<p class="metric-label">昨日用电时段</p>', unsafe_allow_html=True)
    st.write("07:21–08:05  \n18:09–19:10")

with c2:
    st.markdown('<p class="metric-label">建议用电时段</p>', unsafe_allow_html=True)
    st.write("06:18–07:30  \n17:15–18:40")

with c3:
    st.markdown('<p class="metric-label">电费 (¥)</p>', unsafe_allow_html=True)
    st.metric("优化前", "9.10")
    st.metric("优化后", "8.13")

st.markdown("<hr>", unsafe_allow_html=True)  # 分隔线

# 第二行两列（说明）
c4, c5 = st.columns([1, 1.5])
with c4:
    st.markdown('<p class="metric-label">前后舒适度变化</p>', unsafe_allow_html=True)
    st.write("前：1.0000  \n后：0.9375")

with c5:
    st.markdown('<p class="metric-label">说明</p>', unsafe_allow_html=True)
    st.write("优化后整体舒适度略降，但节约约10.6%电费。")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
