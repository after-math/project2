import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np
import pandas as pd
import datetime

# ========== 页面配置 ==========
st.set_page_config(page_title="我的", page_icon="👤", layout="wide")

# ========== 样式优化 ==========
st.markdown("""
<style>
.block-container {padding-top: 1rem; padding-bottom: 0rem;}
.metric-card {
    background-color: #f7f7f7;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.highlight {
    background-color: #f5dada;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}
h2, h3 {font-family: "PingFang SC", "Microsoft YaHei", sans-serif;}
.section {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 20px 25px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ========== 1️⃣ 页面标题 + 日期选择 ==========
col_title, col_date = st.columns([4, 1])

# with col_title:
#     st.markdown("## 👤 我的")

with col_date:
    today = datetime.date.today()
    selected_date = st.date_input(
        "选择日期",
        today,
        min_value=datetime.date(2023, 1, 1),
        max_value=datetime.date(2030, 12, 31),
        format="YYYY-MM-DD",
    )
    st.markdown(
        f"<div style='text-align:center; font-size:14px; color:#666;'>当前日期：{selected_date.strftime('%Y-%m-%d')}</div>",
        unsafe_allow_html=True,
    )

# ========== 2️⃣ 顶部信息卡 ==========
st.markdown('<div class="section">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("**相比上月节省电费**")
    st.markdown("<h1 style='color:#d9534f;'>8.9%</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("**已接入系统的电器数**")
    st.markdown("<h1>15</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="metric-card" style="border:2px dashed #ccc;">', unsafe_allow_html=True)
    st.markdown("**每天平均用电时长**")
    st.markdown("<h1>18.7<sub>h</sub></h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ========== 3️⃣ 电费趋势图（近一月 / 近一周） ==========
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown("### 💹 近一周电费与近一个月电费")

# 以所选日期为基准生成数据（自动更新）
end_date = pd.to_datetime(selected_date)
x_month = pd.date_range(end_date - pd.Timedelta(days=29), end_date)
x_week = pd.date_range(end_date - pd.Timedelta(days=6), end_date)

np.random.seed(int(selected_date.strftime("%Y%m%d")) % 10000)  # ✅ 日期不同 → 随机种子不同
y_month = np.abs(np.random.normal(8, 3, len(x_month))) + np.linspace(0, 2, len(x_month))
y_week = np.abs(np.random.normal(7, 2, len(x_week)))

# 折线图配置（近一个月）
option_month = {
    "title": {"text": "近一个月电费", "left": "center"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": [str(x.date()) for x in x_month]},
    "yAxis": {"type": "value"},
    "series": [{
        "data": list(y_month),
        "type": "line",
        "smooth": True,
        "lineStyle": {"color": "#f59e42", "width": 3},
        "areaStyle": {"color": "rgba(245,158,66,0.15)"}
    }],
}
st_echarts(option_month, height="300px")

# 折线图配置（近一周）
option_week = {
    "title": {"text": "近一周电费", "left": "center"},
    "tooltip": {"trigger": "axis"},
    "xAxis": {"type": "category", "data": [str(x.date()) for x in x_week]},
    "yAxis": {"type": "value"},
    "series": [{
        "data": list(y_week),
        "type": "line",
        "smooth": True,
        "lineStyle": {"color": "#d94b3e", "width": 3},
        "areaStyle": {"color": "rgba(217,75,62,0.15)"}
    }],
}
st_echarts(option_week, height="250px")

st.markdown('</div>', unsafe_allow_html=True)
