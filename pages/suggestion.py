import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# ========== 页面配置 ==========
st.set_page_config(page_title="优化建议", page_icon="💡", layout="centered")

# ========== 全局样式 ==========
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}
.section {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 25px 30px;
    margin-bottom: 25px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
h2, h3, h4 {
    color: #2a3f5f;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ========== 页面标题 ==========
st.markdown("## 💡 优化建议")
st.markdown('<div class="section">', unsafe_allow_html=True)

# ========== 主体内容 ==========
main_col, _ = st.columns([4, 0.0001])
with main_col:
    st.markdown("#### ⚙️ 权重设置")
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        w1 = st.number_input("电费权重", 0.0, 1.0, 0.7, 0.1, key="w1")
    with col2:
        w2 = st.number_input("舒适度权重", 0.0, 1.0, 0.3, 0.1, key="w2")

    st.caption("💬 电费权重越高越节能，舒适度权重越高则更注重使用体验。")

    st.markdown("### ⏱️ 优化前后时段对比（Matplotlib甘特图）")

    # ================= 数据 =================
    data = {
        '设备名称': ['微波炉', '洗碗机', '洗衣机', '电热水器'],
        '原用电时段': [
            '07:00-08:00\n18:00-19:00',
            '09:00-10:00\n21:00-22:00',
            '07:00-08:00\n23:00-24:00',
            '01:00-05:00\n16:00-20:00'
        ],
        '优化后用电时段': [
            '06:00-07:00\n17:00-18:00',
            '08:00-09:00\n20:00-21:00',
            '06:00-07:00\n17:00-18:00',
            '01:00-05:00\n16:00-20:00'
        ]
    }
    df = pd.DataFrame(data)

    # ================= 参数 =================
    bar_height = 0.35
    colors = {"before": "#3B60E4", "after": "#F6A23C"}

    # ================= 绘图 =================
    fig, ax = plt.subplots(figsize=(10, 5))

    for i, row in df.iterrows():
        # 原时段
        for seg in row['原用电时段'].split('\n'):
            s, e = seg.split('-')
            s_h, e_h = int(s.split(':')[0]), int(e.split(':')[0])
            ax.barh(i - bar_height / 2, e_h - s_h, left=s_h,
                    height=bar_height, color=colors["before"], alpha=0.8)
        # 优化后时段
        for seg in row['优化后用电时段'].split('\n'):
            s, e = seg.split('-')
            s_h, e_h = int(s.split(':')[0]), int(e.split(':')[0])
            ax.barh(i + bar_height / 2, e_h - s_h, left=s_h,
                    height=bar_height, color=colors["after"], alpha=0.8)

    # 坐标轴与图例
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['设备名称'], fontsize=11)
    ax.set_xlabel('时间（小时）', fontsize=12)
    ax.set_title('优化前后时段对比', fontsize=14, pad=12)
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 5))
    ax.set_xticklabels([f"{h}:00" for h in range(0, 25, 5)], fontsize=10)
    ax.grid(axis='x', linestyle='--', alpha=0.4)

    blue_patch = mpatches.Patch(color=colors["before"], label='原用电时段', alpha=0.8)
    orange_patch = mpatches.Patch(color=colors["after"], label='优化后用电时段', alpha=0.8)
    ax.legend(handles=[blue_patch, orange_patch], loc='upper right')

    plt.tight_layout()
    st.pyplot(fig)

# ========== 优化前后表格 ==========
st.markdown("### 📊 优化前后目标对比")
st.markdown("<div style='font-size:18px; font-weight:500;'>请选择要查看的电器</div>", unsafe_allow_html=True)
device = st.selectbox("", ["微波炉", "电热水器", "洗碗机"])

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
.highlight {
    background-color: #e8f4ff;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
