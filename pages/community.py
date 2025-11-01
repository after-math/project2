# pages/community.py
import streamlit as st
from datetime import datetime, timedelta
import base64
from io import BytesIO

from traitlets import default

st.set_page_config(page_title="社区", page_icon="🌐", layout="wide")

# -------------------- 样式 --------------------
st.markdown("""
<style>
:root { --card-bg:#ffffff; --muted:#6b7280; }
[data-testid="stAppViewContainer"]{ background: #f7f9fc; }
.section-title{font-weight:700;font-size:20px;margin:4px 0 12px 2px}
.post-card{
  background:var(--card-bg);border:1px solid #eef1f6;border-radius:16px;
  padding:14px 16px;margin-bottom:14px;box-shadow:0 2px 8px rgba(0,0,0,.03);
}
.post-head{display:flex;gap:10px;align-items:center;margin-bottom:6px}
.post-avatar{width:34px;height:34px;border-radius:50%;object-fit:cover;border:2px solid #e6ebf3}
.post-name{font-weight:600}
.post-meta{color:var(--muted);font-size:12px}
.post-tags{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}
.tag{background:#eef6ff;border:1px solid #d6e7ff;color:#2563eb;
     border-radius:999px;padding:2px 8px;font-size:12px}
.post-actions{display:flex;gap:12px;color:#374151;font-size:13px;margin-top:6px}
.post-actions span{cursor:pointer;padding:4px 6px;border-radius:8px}
.post-actions span:hover{background:#f1f5f9}
.comment-box{margin-top:8px;padding-top:8px;border-top:1px dashed #e5e7eb}
.sidebar-card{background:#fff;border:1px solid #eef1f6;border-radius:14px;padding:14px;margin-bottom:14px}
.stat{display:flex;justify-content:space-between;color:#4b5563;font-size:13px;margin:6px 0}
.small{color:#6b7280;font-size:12px}
input, textarea{font-family: 'PingFang SC','Microsoft YaHei',system-ui}
</style>
""", unsafe_allow_html=True)

# -------------------- 数据模型 --------------------
if "comm_posts" not in st.session_state:
    # 预置几条示例贴
    now = datetime.now()
    st.session_state.comm_posts = [
        {
            "id": 1,
            "user": "🔧 电费优化官",
            "avatar": None,
            "time": now - timedelta(minutes=26),
            "text": "今天把热水器错峰到 06:20-07:10，电费立减 11%，体感无差～",
            "tags": ["节能技巧","热水器"],
            "likes": 12, "star": 4,
            "comments": [{"user":"小陶","text":"实测也行！","time": now - timedelta(minutes=10)}],
            "images": []
        },
        {
            "id": 2,
            "user": "📊 数据侠",
            "avatar": None,
            "time": now - timedelta(hours=2),
            "text": "分享一张昨晚负荷曲线，谁要一起做个预测小游戏？",
            "tags": ["数据","负荷预测"],
            "likes": 7, "star": 2, "comments": [], "images": []
        },
        {
            "id": 3,
            "user": "🧼 节能小分队",
            "avatar": None,
            "time": now - timedelta(days=1, hours=3),
            "text": "洗碗机放到 21:00 后启动，噪声更小，电价也低。",
            "tags": ["洗碗机","体验感"],
            "likes": 19, "star": 9, "comments": [], "images": []
        },
    ]
    st.session_state.comm_next_id = 4

posts = st.session_state.comm_posts

# -------------------- 工具函数 --------------------
def humanize(dt: datetime) -> str:
    delta = datetime.now() - dt
    if delta.days >= 1:
        return f"{delta.days} 天前"
    m = int(delta.total_seconds()//60)
    if m <= 0: return "刚刚"
    if m < 60: return f"{m} 分钟前"
    return f"{m//60} 小时前"

def add_post(text, tags, images):
    st.session_state.comm_posts.insert(0, {
        "id": st.session_state.comm_next_id,
        "user": "🙂 我",
        "avatar": None,
        "time": datetime.now(),
        "text": text.strip(),
        "tags": [t.strip() for t in tags if t.strip()],
        "likes": 0, "star": 0, "comments": [],
        "images": images or []
    })
    st.session_state.comm_next_id += 1

def b64_of_image(file):
    img_bytes = file.read()
    return "data:image/png;base64," + base64.b64encode(img_bytes).decode()

# -------------------- 顶部工具条 --------------------
left, right = st.columns([3, 1.2])
with left:
    st.markdown('<div class="section-title">🧭 社区</div>', unsafe_allow_html=True)
    q1, q2, q3 = st.columns([2.2, 1.4, 1.2])
    with q1:
        keyword = st.text_input("🔍 搜索帖子 / 话题", value="", placeholder="输入关键词…")
    with q2:
        sort = st.selectbox("排序", ["最新发布","最热互动"])
    with q3:
        tag_filter = st.selectbox("话题筛选", ["全部","节能技巧","热水器","数据","负荷预测","洗碗机","体验感"])

with right:
    with st.container():
        st.markdown('<div class="sidebar-card"><b>📈 今日社区概览</b>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat"><span>帖子数</span><span>{len(posts)}</span></div>', unsafe_allow_html=True)
        total_comments = sum(len(p["comments"]) for p in posts)
        st.markdown(f'<div class="stat"><span>评论数</span><span>{total_comments}</span></div>', unsafe_allow_html=True)
        total_likes = sum(p["likes"] for p in posts)
        st.markdown(f'<div class="stat"><span>点赞数</span><span>{total_likes}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="small">🎯 小贴士：分享你的错峰用电经验，帮助更多人省钱～</div></div>', unsafe_allow_html=True)

# -------------------- 发帖框 --------------------
with st.container():
    st.markdown('<div class="section-title">✍️ 发帖</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1.2])
    with c1:
        text = st.text_area("今天想分享什么？（支持换行）", height=120, label_visibility="collapsed",
                            placeholder="例如：分享一下我家的洗衣机/热水器错峰经验…")
        tcol1, tcol2 = st.columns([3,2])
        with tcol1:
            tag_input = st.text_input("添加话题（用逗号分隔）", placeholder="如：节能技巧, 热水器")
        with tcol2:
            uploads = st.file_uploader("可选：上传图片（最多2张）", type=["png","jpg","jpeg"], accept_multiple_files=True)
    with c2:
        st.write("")
        st.write("")
        if st.button("🚀 发布", use_container_width=True, type="primary",
                     disabled=(not text.strip())):
            imgs = []
            if uploads:
                for f in uploads[:2]:
                    imgs.append(b64_of_image(f))
            add_post(text, tag_input.split(","), imgs)
            st.success("已发布！")
            st.experimental_rerun()

st.markdown("---")

# -------------------- 列表过滤 & 排序 --------------------
def match(p):
    if tag_filter != "全部" and tag_filter not in p["tags"]:
        return False
    if keyword:
        kw = keyword.strip()
        in_text = kw in p["text"]
        in_tags = any(kw in t for t in p["tags"])
        return in_text or in_tags or kw in p["user"]
    return True

filtered = [p for p in posts if match(p)]
if sort == "最新发布":
    filtered.sort(key=lambda x: x["time"], reverse=True)
else:
    filtered.sort(key=lambda x: (x["likes"]*3 + len(x["comments"])*2 + x["star"]), reverse=True)

# -------------------- 分页 --------------------
PAGE_SIZE = 5
page_total = max(1, (len(filtered)+PAGE_SIZE-1)//PAGE_SIZE)
page = st.segmented_control("分页", options=[str(i) for i in range(1, page_total+1)],
                            default="1" if page_total else "1", key="comm_page")
page_idx = int(page)-1
page_items = filtered[page_idx*PAGE_SIZE:(page_idx+1)*PAGE_SIZE]

# -------------------- 渲染帖子 --------------------
for p in page_items:
    with st.container():
        st.markdown('<div class="post-card">', unsafe_allow_html=True)
        # 头像与头部
        a1, a2 = st.columns([0.08, 0.92])
        with a1:
            if p["avatar"]:
                st.image(p["avatar"], use_container_width=True)
            else:
                st.markdown(f'<img class="post-avatar" src="https://api.dicebear.com/7.x/identicon/svg?seed={p["user"]}"/>',
                            unsafe_allow_html=True)
        with a2:
            st.markdown(
                f'<div class="post-head"><div class="post-name">{p["user"]}</div>'
                f'<div class="post-meta">· {humanize(p["time"])}</div></div>', unsafe_allow_html=True)
            st.markdown(p["text"])
            if p["images"]:
                ig = st.columns(len(p["images"]))
                for i, img in enumerate(p["images"]):
                    with ig[i]:
                        st.image(img, use_container_width=True)
            if p["tags"]:
                st.markdown('<div class="post-tags">' +
                            "".join([f'<span class="tag">#{t}</span>' for t in p["tags"]]) +
                            '</div>', unsafe_allow_html=True)

            # 互动按钮
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button(f"👍 {p['likes']}", key=f"like_{p['id']}", use_container_width=True):
                    p["likes"] += 1; st.experimental_rerun()
            with c2:
                if st.button(f"⭐ {p['star']}", key=f"star_{p['id']}", use_container_width=True):
                    p["star"] += 1; st.experimental_rerun()
            with c3:
                st.write("")
            with c4:
                togg = st.toggle("💬 评论", key=f"toggle_{p['id']}")
            # 评论区
            if togg:
                st.markdown('<div class="comment-box">', unsafe_allow_html=True)
                for cm in p["comments"]:
                    st.markdown(f"**{cm['user']}**：{cm['text']}  "
                                f"<span class='small'>· {humanize(cm['time'])}</span>", unsafe_allow_html=True)
                new_comment = st.text_input("写下你的看法…", key=f"cmt_input_{p['id']}")
                ccol1, ccol2 = st.columns([1,4])
                with ccol1:
                    if st.button("发送", key=f"cmt_btn_{p['id']}") and new_comment.strip():
                        p["comments"].append({"user":"🙂 我","text":new_comment.strip(),"time":datetime.now()})
                        st.experimental_rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------- 右栏：热门话题/公告 --------------------
with right:
    with st.container():
        st.markdown('<div class="sidebar-card"><b>🔥 热门话题</b><br>', unsafe_allow_html=True)
        hot = {}
        for p in posts:
            for t in p["tags"]:
                hot[t] = hot.get(t, 0) + 1
        hot_items = sorted(hot.items(), key=lambda x: x[1], reverse=True)[:8]
        if hot_items:
            for t, n in hot_items:
                st.markdown(f"- #{t}  <span class='small'>×{n}</span>", unsafe_allow_html=True)
        else:
            st.caption("暂无话题～")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="sidebar-card"><b>📢 公告</b>', unsafe_allow_html=True)
        st.markdown("- 本周优选：发布高质量节能经验可获特殊徽章\n- 违规内容将被删除，请友善交流")
        st.markdown("</div>", unsafe_allow_html=True)
