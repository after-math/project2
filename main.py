import streamlit as st
import base64

# ======== 头像转 Base64 ========
with open("头像.jpg", "rb") as f:
    img_bytes = f.read()
    img_base64 = base64.b64encode(img_bytes).decode()

# ======== 页面配置 ========
st.set_page_config(page_title="智能优解", page_icon="🔐", layout="centered")
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
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# ======== 登录页 ========
def login_page():
    st.title("🔐 登录页面")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if username == "admin" and password == "123456":
            st.session_state.logged_in = True
            st.success("✅ 登录成功！")
            st.rerun()
        else:
            st.error("❌ 用户名或密码错误")

# ======== 登录成功后的主界面 ========
if st.session_state.logged_in:

    # ==================== 💠 侧边栏头像放在顶部 ====================
    st.markdown(f"""
    <style>
    /* 侧边栏整体样式 */
    [data-testid="stSidebar"] {{
        background-color: #f8f9fb;
        font-family: 'PingFang SC','Microsoft YaHei';
    }}

    /* ======== 头像卡片区域 ======== */
    [data-testid="stSidebar"] > div:first-child::before {{
        content: "";
        display: block;
        margin: 25px auto 0 auto;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: url("data:image/jpeg;base64,{img_base64}") center/cover no-repeat;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 3px solid #e0e6ef;
    }}

    /* ======== 名字与欢迎语 ======== */
    [data-testid="stSidebar"] > div:first-child::after {{
        # content: "程嘉明\\A欢迎回来 👋";
        white-space: pre;
        display: block;
        text-align: center;
        font-size: 14px;
        color: #333;
        margin-top: 10px;
        line-height: 1.6;
        padding-bottom: 12px;
        border-bottom: 1px solid #e5e7eb;
    }}

    /* ======== 导航按钮间距优化 ======== */
    button[kind="secondary"] {{
        background-color: transparent !important;
        color: #333 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.7rem 1rem !important;
        margin: 50px 10 !important;   /* ✅ 增大间距 */
        font-size: 15px !important;
        transition: all 0.2s ease-in-out;
    }}

    button[kind="secondary"]:hover {{
        background-color: rgba(0, 120, 215, 0.08) !important;
        color: #0078D7 !important;
    }}

    button[kind="secondary"]:focus {{
        background-color: rgba(0, 120, 215, 0.15) !important;
        font-weight: 600 !important;
        color: #0078D7 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ==================== 页面导航定义 ====================
    page_home = st.Page("pages/home.py", title="🏠 首页")
    page_information = st.Page("pages/information_on_electricity_consumption.py", title="💡 用电情况")
    page_suggestion = st.Page("pages/suggestion.py", title="🧭 用电建议")
    page_community = st.Page("pages/community.py", title="🌐 社区")
    page_setting = st.Page("pages/setting.py", title="⚙️ 设置")

    nav = st.navigation(pages=[
        page_home,
        page_information,
        page_suggestion,
        page_community,
        page_setting
    ])
    nav.run()

# ==================== 未登录时 ====================
else:
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom right, #eef2f7, #ffffff);
    }
    </style>
    """, unsafe_allow_html=True)
    login_page()
