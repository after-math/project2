import streamlit as st
import base64
from pathlib import Path

# ========== 页面配置 ==========
st.set_page_config(page_title="智能优解系统登录", page_icon="🔐", layout="wide")

# ========== 图片资源 ==========
IMG_PATH = Path("背景.jpg")
AVATAR_PATH = Path("头像.jpg")

def to_b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()

bg_b64 = to_b64(IMG_PATH)
avatar_b64 = to_b64(AVATAR_PATH)

# ========== Session 初始化 ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ========== 登录页样式 ==========
LOGIN_CSS = f"""
<style>
[data-testid="stSidebar"], header[data-testid="stHeader"] {{
    display: none !important;
}}

.block-container {{
    max-width: 1100px;
    margin: 0 auto !important;
    padding-top: 40px;
}}

.page {{
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    gap: 30px;
    align-items: center;
}}

.hero {{
    background: url("data:image/png;base64,{bg_b64}") center/cover no-repeat;
    height: 500px;
    border-radius: 12px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.12);
}}

.card {{
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    padding: 36px 30px;
}}

.card h2 {{
    color: #1a3c8b;
    font-size: 22px;
    margin-bottom: 12px;
}}

.card p {{
    color: #666;
    font-size: 14px;
    margin-bottom: 24px;
}}

.stTextInput > div > div input {{
    height: 36px !important;
    border-radius: 8px !important;
}}

.stButton > button {{
    width: 100%;
    height: 38px;
    border-radius: 8px;
    background: #1a73e8 !important;
    color: white !important;
    font-weight: 600;
}}
</style>
"""

# ========== 登录页 ==========
def login_page():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown('<div class="page">', unsafe_allow_html=True)

    st.markdown('<div class="hero"></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2>🔐 智能优解系统登录</h2>", unsafe_allow_html=True)
    st.markdown("<p>双智协同下居民负荷分解与柔性用能决策优化平台</p>", unsafe_allow_html=True)

    username = st.text_input("用户名", placeholder="请输入用户名")
    password = st.text_input("密码", placeholder="请输入密码", type="password")

    if st.button("登 录"):
        if username == "admin" and password == "123456":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ 登录成功！")
            st.rerun()
        else:
            st.error("❌ 用户名或密码错误")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ========== 主系统导航 ==========
def main_system():
    # 侧边栏样式（头像 + 欢迎语）
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background-color: #f8f9fb;
        font-family: 'PingFang SC','Microsoft YaHei';
    }}
    [data-testid="stSidebar"]::before {{
        content: "";
        display: block;
        width: 120px;
        height: 120px;
        margin: 20px auto 10px;
        border-radius: 50%;
        background: url("data:image/jpeg;base64,{avatar_b64}") center/cover no-repeat;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        border: 3px solid #e0e6ef;
    }}
    [data-testid="stSidebar"]::after {{
        content: "{st.session_state.username}\\A欢迎回来 👋";
        white-space: pre;
        display: block;
        text-align: center;
        margin-top: 12px;
        color: #444;
        font-size: 15px;
        padding-bottom: 12px;
        border-bottom: 1px solid #e6e9ef;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 页面导航定义（main不显示）
    home = st.Page("pages/home.py", title="🏠 首页")
    info = st.Page("pages/information_on_electricity_consumption.py", title="💡 用电情况")
    sugg = st.Page("pages/suggestion.py", title="🧭 用电建议")
    comm = st.Page("pages/community.py", title="🌐 社区")
    sett = st.Page("pages/setting.py", title="⚙️ 设置")

    nav = st.navigation(
        pages=[home, info, sugg, comm, sett]
    )

    # 添加退出登录按钮
    with st.sidebar:
        st.divider()
        if st.button("退出登录"):
            st.session_state.logged_in = False
            st.rerun()

    # 运行导航
    nav.run()


# ========== 路由控制 ==========
if st.session_state.logged_in:
    main_system()
else:
    login_page()
