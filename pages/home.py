import streamlit as st
from streamlit_echarts import st_echarts
import numpy as np
import pandas as pd
import datetime

# ========== 页面配置 ==========
st.set_page_config(page_title="我的", page_icon="👤", layout="centered",)
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

# ========== 样式优化 ==========
st.markdown("""
<style>
.block-container {padding-top: 3rem; padding-bottom: 0rem;}
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

with col_title:
     st.markdown("## 👤 我的")

with col_date:
    # 获取今天的日期（datetime.date 类型），例如 2025-10-27
    today = datetime.date.today()

    # 创建一个日期选择器组件（Date Picker）
    selected_date = st.date_input(
        '',                             # 第一个参数是标签文本，这里为空字符串表示不显示标签
        today,                          # 默认选中日期，这里设为“今天”
        min_value=datetime.date(2023, 1, 1),   # 可选择的最早日期（限制范围）
        max_value=datetime.date(2030, 12, 31), # 可选择的最晚日期
        format="YYYY-MM-DD",             # 日期显示格式（年-月-日）
    )

    st.markdown(
        f"<div style='text-align:center; font-size:14px; color:#666;'>当前日期：{today.strftime('%Y-%m-%d')}</div>",
        unsafe_allow_html=True,
    )

# ========== 2️⃣ 顶部信息卡 ==========
st.markdown('<div class="section">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    #st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("### 相比上月节省电费")
    st.markdown("<h1 style='color:#d9534f'>8.9%</h1>", unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)

with c2:
    #st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### 已接入系统的电器数")
    st.markdown("<h1>15</h1>", unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)

with c3:
    #st.markdown('<div class="metric-card" style="border:2px dashed #ccc;">', unsafe_allow_html=True)
    st.markdown("### 每天平均用电时长")
    st.markdown("<h1>18.7h</h1>", unsafe_allow_html=True)
    # st.markdown('</div>', unsafe_allow_html=True)

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
    # ======================== 图表标题 ========================
    "title": {
        "text": "📈 近一个月电费趋势",     # 标题内容
        "left": "center",                  # 标题居中
        "textStyle": {                     # 标题样式设置
            "fontSize": 18,
            "fontWeight": "bold",
            "color": "#333"
        }
    },

    # ======================== 提示框 ========================
    "tooltip": {
        "trigger": "axis",                 # 在坐标轴上触发，显示该点所有系列值
        "axisPointer": {                   # 指示线样式
            "type": "line",                # 可选：'line'（竖线）、'shadow'（阴影）
            "lineStyle": {"color": "#aaa", "width": 1, "type": "dashed"}
        },
        "backgroundColor": "rgba(255,255,255,0.9)",  # 白底半透明
        "textStyle": {"color": "#333"},
        "borderWidth": 0,
        "formatter": "日期：{b}<br/>电费：{c} 度"  # 自定义提示内容格式
    },

    # ======================== 图表绘图区边距 ========================
    "grid": {
        "left": "8%",                      # 左边距
        "right": "8%",                     # 右边距
        "top": "15%",                      # 上边距
        "bottom": "10%",                   # 下边距
        "containLabel": True               # 保证标签不会被裁剪
    },

    # ======================== X 轴（横轴） ========================
    "xAxis": {
        "type": "category",                # 类别轴（日期字符串）
        "data": [str(x.date()) for x in x_month],  # 日期序列
        "name": "日期",                    # 坐标轴名称
        "axisLine": {"lineStyle": {"color": "#999"}},  # 轴线颜色
        "axisLabel": {
            "rotate": 40,                  # 标签旋转角度，防止日期重叠
            "color": "#555",
            "fontSize": 11
        },
        "boundaryGap": False               # 坐标轴两端不留白
    },

    # ======================== Y 轴（纵轴） ========================
    "yAxis": {
        "type": "value",                   # 数值轴
        "name": "电量（度）",               # 坐标轴名称
        "nameTextStyle": {"fontSize": 13, "color": "#444"},
        "axisLine": {"show": False},       # 不显示 y 轴线
        "axisTick": {"show": False},       # 不显示刻度线
        "splitLine": {"lineStyle": {"color": "#eee"}}  # 分隔线颜色
    },

    # ======================== 折线序列（主图数据） ========================
    "series": [{
        "name": "电费",                    # 系列名称，用于图例和 tooltip
        "data": list(y_month),             # Y 轴对应的数据
        "type": "line",                    # 折线图
        "smooth": True,                    # 平滑曲线
        "symbol": "circle",                # 数据点形状
        "symbolSize": 6,                   # 数据点大小
        "itemStyle": {"color": "#f59e42"}, # 折线点颜色
        "lineStyle": {"color": "#f59e42", "width": 3}, # 折线样式
        "areaStyle": {                     # 面积填充（渐变色）
            "color": {
                "type": "linear",
                "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [
                    {"offset": 0, "color": "rgba(245,158,66,0.35)"},  # 顶部颜色
                    {"offset": 1, "color": "rgba(245,158,66,0.05)"}   # 底部渐变
                ]
            }
        },
        "emphasis": {                      # 鼠标悬停高亮样式
            "focus": "series",
            "itemStyle": {"color": "#ff7e00"}  # 高亮时点的颜色
        }
    }],

    # ======================== 动画与交互 ========================
    "animationDuration": 1500,             # 动画时长（毫秒）
    "animationEasing": "cubicOut",         # 动画缓动曲线（自然减速）
}

st_echarts(option_month, height="300px")

# ================================
# 折线图配置（近一周电费趋势）
# ================================
option_week = {
    # ======================== 图表标题 ========================
    "title": {
        "text": "⚡ 近一周电费趋势",         # 图表标题文字
        "left": "center",                  # 居中显示
        "textStyle": {                     # 标题样式
            "fontSize": 18,
            "fontWeight": "bold",
            "color": "#333"
        }
    },

    # ======================== 提示框 ========================
    "tooltip": {
        "trigger": "axis",                 # 在坐标轴上触发，显示该点所有系列数据
        "axisPointer": {                   # 鼠标悬停时的指示线样式
            "type": "line",
            "lineStyle": {"color": "#aaa", "width": 1, "type": "dashed"}
        },
        "backgroundColor": "rgba(255,255,255,0.9)",  # 白底、半透明背景
        "textStyle": {"color": "#333"},
        "borderWidth": 0,
        "formatter": "日期：{b}<br/>电费：{c} 度"    # 自定义提示文本
    },

    # ======================== 绘图区边距 ========================
    "grid": {
        "left": "8%",                      # 左边距
        "right": "8%",                     # 右边距
        "top": "15%",                      # 上边距
        "bottom": "10%",                   # 下边距
        "containLabel": True               # 防止标签被裁剪
    },

    # ======================== X 轴（日期） ========================
    "xAxis": {
        "type": "category",                # 类别轴（日期字符串）
        "data": [str(x.date()) for x in x_week],  # 一周日期序列
        "name": "日期",                    # 坐标轴名称
        "axisLine": {"lineStyle": {"color": "#999"}},  # 坐标轴线颜色
        "axisLabel": {
            "rotate": 30,                  # 日期文字旋转角度，防止重叠
            "color": "#555",
            "fontSize": 11
        },
        "boundaryGap": False               # 坐标轴两端不留白
    },

    # ======================== Y 轴（电费） ========================
    "yAxis": {
        "type": "value",                   # 数值轴
        "name": "电量（度）",               # 坐标轴标题
        "nameTextStyle": {"fontSize": 13, "color": "#444"},
        "axisLine": {"show": False},       # 不显示 y 轴线
        "axisTick": {"show": False},       # 不显示刻度
        "splitLine": {"lineStyle": {"color": "#eee"}}  # 背景分隔线
    },

    # ======================== 数据序列（折线） ========================
    "series": [{
        "name": "电费",                    # 系列名称
        "data": list(y_week),              # 一周内电费数据
        "type": "line",                    # 折线图类型
        "smooth": True,                    # 平滑曲线
        "symbol": "circle",                # 数据点形状
        "symbolSize": 6,                   # 数据点大小
        "itemStyle": {"color": "#d94b3e"}, # 折线点颜色（红橙）
        "lineStyle": {"color": "#d94b3e", "width": 3}, # 折线样式
        "areaStyle": {                     # 区域渐变填充
            "color": {
                "type": "linear",
                "x": 0, "y": 0, "x2": 0, "y2": 1,
                "colorStops": [
                    {"offset": 0, "color": "rgba(217,75,62,0.35)"},  # 顶部
                    {"offset": 1, "color": "rgba(217,75,62,0.05)"}   # 底部渐变
                ]
            }
        },
        "emphasis": {                      # 鼠标悬停高亮效果
            "focus": "series",
            "itemStyle": {"color": "#ff6b4a"}
        }
    }],

    # ======================== 动画效果 ========================
    "animationDuration": 1500,             # 动画时长（毫秒）
    "animationEasing": "cubicOut",         # 缓动曲线
}

st_echarts(option_week, height="250px")

st.markdown('</div>', unsafe_allow_html=True)
