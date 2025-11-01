import streamlit as st
import base64
from pathlib import Path

# ========== 基本配置 ==========
st.set_page_config(page_title="智能优解登录", page_icon="🔐", layout="wide")

# ========== 资源准备 ==========
IMG_PATH = Path("背景.jpg")   # ← 左侧展示的大图，换成你的图片文件
assert IMG_PATH.exists(), "找不到 背景.jpg，请把展示图片放在同目录下或修改 IMG_PATH。"

def to_b64(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()

hero_b64 = to_b64(IMG_PATH)

# ========== 页面状态 ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ========== 样式 ==========
LOGIN_CSS = f"""
<style>
/* 隐藏登录页的侧边栏和顶部 */
[data-testid="stSidebar"] {{ display: none !important; }}
header[data-testid="stHeader"] {{ display: none !important; }}

/* 整页背景与容器宽度 */
.block-container {{
    padding-top: 24px !important;
    padding-bottom: 24px !important;
    max-width: 1200px !important;   /* 页面最大宽度 */
    margin: 0 auto !important;      /* 居中 */
}}

/* 顶部标题行（可按需隐藏） */
.topbar {{
    display: flex;
    align-items: center;
    gap: 10px;
    color: #0b3d91;
    font-weight: 600;
    margin: 8px 0 16px 0;
    font-size: 20px;
}}

/* 主体两栏布局 */
.page {{
    display: grid;
    grid-template-columns: 2fr 1fr;  /* 左图 : 右卡片 = 2:1 */
    gap: 28px;
    align-items: center;
}}

/* 左侧大图 */
.hero {{
    width: 100%;
    aspect-ratio: 16 / 9;           /* 比例可按需改 */
    background: url("data:image/png;base64,{hero_b64}") center/cover no-repeat;
    border-radius: 10px;
    box-shadow: 0 6px 20px rgba(0,0,0,.12);
    border: 1px solid #eef1f5;
}}

/* 右侧登录卡片 */
.card {{
    width: 100%;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 18px rgba(0,0,0,.08);
    border: 1px solid #eef1f5;
    padding: 26px 24px 20px 24px;
    font-family: "PingFang SC","Microsoft YaHei",system-ui,Arial;
}}

.card h3 {{
    margin: 0 0 18px 0;
    font-size: 18px;
    color: #1a3c8b;
    font-weight: 700;
}}

.card .hint {{
    margin-bottom: 12px;
    color: #666;
    font-size: 13px;
}}

.card .forget {{
    text-align: right;
    margin-top: 6px;
    font-size: 13px;
}}
.card .forget a {{
    color: #1a73e8;
    text-decoration: none;
}}
.card .forget a:hover {{ text-decoration: underline; }}

/* 让输入控件更紧凑 */
.card .stTextInput > div > div input {{
    height: 38px !important;
}}
.card .stTextInput, .card .stPasswordInput {{
    margin-bottom: 10px !important;
}}

/* 登录按钮风格 */
.card .stButton > button {{
    width: 100%;
    height: 40px;
    border-radius: 6px;
    font-weight: 600;
    background: #1a73e8 !important;
    color: #fff !important;
    border: none;
}}
.card .stButton > button:hover {{
    background: #0c5dd6 !important;
}}
</style>
"""

# ========== 登录页 ==========
def login_page():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)

    # 顶部标题（可改为你的系统名或隐藏）
    st.markdown(
        '<div class="topbar">🧠 智能优解电力优化平台</div>',
        unsafe_allow_html=True
    )

    # 两栏：左图 + 右侧登录卡片
    st.markdown('<div class="page">', unsafe_allow_html=True)

    # 左图
    st.markdown('<div class="hero"></div>', unsafe_allow_html=True)

    # 右侧登录卡片（用正常的 Streamlit 控件）
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3>用户登录</h3>', unsafe_allow_html=True)
    st.markdown('<div class="hint">请输入用户名与密码完成登录。</div>', unsafe_allow_html=True)

    username = st.text_input("用户名", placeholder="请输入用户名", label_visibility="visible", key="u")
    password = st.text_input("密码", placeholder="请输入密码", type="password", label_visibility="visible", key="p")

    if st.button("登 录", use_container_width=True):
        if username == "admin" and password == "123456":
            st.session_state.logged_in = True
            st.success("✅ 登录成功")
            st.experimental_rerun()
        else:
            st.error("❌ 用户名或密码错误")

    st.markdown('<div class="forget"><a href="#">忘记密码了？</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # /card

    st.markdown('</div>', unsafe_allow_html=True)  # /page

# ========== 主页面（示例） ==========
def main_page():
    st.success("登录成功，这里是主页面内容（示例）。")
    st.write("你可以在这里放导航、图表、表格等。")
    if st.button("退出登录"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# ========== 路由 ==========
if st.session_state.logged_in:
    main_page()
else:
    login_page()
