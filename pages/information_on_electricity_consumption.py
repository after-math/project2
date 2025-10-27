import streamlit as st
import numpy as np
import datetime
from streamlit_echarts import st_echarts

# ========== 页面配置 ==========
st.set_page_config(page_title="用电情况监测", page_icon="⚡", layout="wide")
# 在 Streamlit 中强制设置 viewport
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
/* 保证移动端布局正常 */
html, body {
    zoom: 1.0 !important;
    -webkit-text-size-adjust: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ========== 页面标题与日期选择 ==========
col_title, col_date = st.columns([4, 1])

with col_title:
    st.title("📊 家用电器功率监测面板")

with col_date:
    today = datetime.date.today()
    selected_date = st.date_input(
        "选择日期", 
        today, 
        min_value=datetime.date(2023, 1, 1),
        max_value=datetime.date(2030, 12, 31),
        format="YYYY-MM-DD"
    )
    # 日期选择器标题字体太大时可以隐藏
    st.markdown(
        f"<div style='text-align:center; font-size:14px; color:#666;'>当前日期：{selected_date.strftime('%Y-%m-%d')}</div>",
        unsafe_allow_html=True
    )

# ========== 模拟数据函数 ==========
def generate_data(seed, base=1000, noise=300, n=100):
    np.random.seed(seed)
    y = base + noise * np.random.randn(n)
    y = np.clip(y, 400, 1600)
    x = [f"{i/6:.1f}" for i in range(n)]  # 分钟
    return x, list(y)

# ========== 通用绘图函数 ==========
def render_chart(title, color, seed):
    x, y = generate_data(seed)
    option = {
        "title": {"text": title, "left": "center", "top": 10, "textStyle": {"fontSize": 16}},
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "name": "时间 (min)",
            "data": x,
            "boundaryGap": False,
            "axisLine": {"lineStyle": {"color": "#888"}}
        },
        "yAxis": {
            "type": "value",
            "name": "功率 /W",
            "min": 0,
            "max": 1800,
            "axisLine": {"lineStyle": {"color": "#888"}}
        },
        "dataZoom": [
            {"type": "inside"},  # ✅ 支持鼠标滚轮缩放
            {"type": "slider"}   # ✅ 可拖动条（可删除）
        ],
        "series": [{
            "data": y,
            "type": "line",
            "smooth": True,
            "symbol": "none",
            "lineStyle": {"color": color, "width": 3},
            "areaStyle": {"color": color, "opacity": 0.1}
        }],
        "grid": {"left": "10%", "right": "5%", "bottom": "15%", "top": "15%"},
    }

    st_echarts(options=option, height="320px", key=title)

# ========== 页面布局（双列） ==========
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🫧 热水器")
    render_chart("热水器功率变化曲线", "#3B82F6", 0)

    st.markdown("### 🍽️ 洗碗机")
    render_chart("洗碗机功率变化曲线", "#F59E0B", 2)

with col2:
    st.markdown("### 📡 微波炉")
    render_chart("微波炉功率变化曲线", "#10B981", 1)

    st.markdown("### 👕 洗衣机")
    render_chart("洗衣机功率变化曲线", "#8B5CF6", 3)
