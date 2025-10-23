import streamlit as st



# ---------------- 页面配置 ----------------
st.set_page_config(page_title="智能优解", page_icon="🔐", layout="centered")

# ---------------- 状态初始化 ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- 登录页 ----------------
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

# ---------------- 主导航定义 ----------------
if st.session_state.logged_in:
    page_suggestion = st.Page("pages/suggestion.py", title="用电建议", icon="📝")
    page_home = st.Page("pages/home.py", title="首页", icon="📖")
    page_community = st.Page("pages/community.py", title="社区", icon="📝")
    page_information_on_electricity_consumption = st.Page("pages/information_on_electricity_consumption.py", title="用电情况", icon="📝")
    page_setting = st.Page("pages/setting.py", title="设置", icon="📝")
    nav = st.navigation(pages=[page_home,page_suggestion,page_community,page_information_on_electricity_consumption , page_setting])
    nav.run()
else:
    # 隐藏侧边栏
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
    login_page()
