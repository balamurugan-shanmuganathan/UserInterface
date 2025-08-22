# app.py
from io import BytesIO
import base64
from datetime import datetime
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="HEDISAbstractor.AI", layout="wide")

# ----------------------------- Styles -----------------------------
st.markdown("""
<style>
.block-container{padding-top:.8rem; padding-bottom:2rem;}
/* Orange banner */
.app-header{
  background:linear-gradient(90deg,#ff6a00,#ff8e3c);
  color:#fff; border-radius:14px; padding:12px 18px; margin-bottom:16px;
  display:flex; align-items:center; justify-content:space-between;
  box-shadow:0 10px 30px rgba(255,138,76,.25);
}
.brand{font-weight:800; font-size:22px; letter-spacing:.2px}
.brand small{opacity:.95; font-weight:700; margin-left:8px}
.pill{display:inline-flex; align-items:center; gap:8px; background:rgba(255,255,255,.18);
     padding:6px 10px; border-radius:999px; font-weight:600;}
.avatar{width:28px; height:28px; border-radius:50%; background:#fff; color:#ff6a00; font-weight:800;
        display:inline-flex; align-items:center; justify-content:center;}
/* Upload bar */
.upload-card{background:#fafafa; border:1px solid #eee; border-radius:12px; padding:16px;}
/* Chat card */
.chat-card{
  border:2px solid #ffa65c; border-radius:12px; padding:16px; background:#fff; box-shadow:0 3px 10px rgba(0,0,0,.04);
}
.msg{border-radius:10px; padding:.6rem .8rem; margin:.25rem 0; background:#f9fafb; border:1px solid #e5e7eb;}
.msg.assistant{background:#eef6ff; border-color:#dbeafe;}
.small{color:#6b7280; font-size:12px;}
/* Lower area */
.soft{background:#fafafa; border:1px solid #eee; border-radius:12px; padding:14px;}
</style>
""", unsafe_allow_html=True)

# ----------------------------- Header -----------------------------
def header():
    st.markdown("""
    <div class="app-header">
      <div class="brand">HEDISAbstractor.AI <small>EXL</small></div>
      <div style="display:flex; gap:10px; align-items:center">
        <span class="pill">Deploy</span>
        <span class="pill"><span class="avatar">A</span> Hi, Ayush</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------- Avatar -----------------------------
def create_avatar(letter: str, size=28, bg="#fff", fg="#ff6a00"):
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, size, size), fill=bg)
    try:
        font = ImageFont.truetype("arial.ttf", size=int(size * 0.6))
    except:
        font = ImageFont.load_default()
    try:
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width, text_height = bbox[2]-bbox[0], bbox[3]-bbox[1]
    except AttributeError:
        text_width, text_height = font.getsize(letter)
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 2
    draw.text((text_x, text_y), letter, font=font, fill=fg)
    return img

# ----------------------------- Sidebar -----------------------------
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Summarization", "New File Intake", "ReviewMember", "Data Repository", "App Statistics"],
    index=0
)

# ----------------------------- Helpers -----------------------------
def embed_pdf(file_bytes: bytes, height=700):
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    html = f"""<iframe src="data:application/pdf;base64,{b64}#view=FitH" width="100%" height="{height}" type="application/pdf"></iframe>"""
    st.components.v1.html(html, height=height+5, scrolling=True)

def render_pdf_page(file_bytes: bytes, page_num: int):
    try:
        from pdf2image import convert_from_bytes
        imgs = convert_from_bytes(file_bytes, dpi=150, first_page=page_num, last_page=page_num)
        return imgs[0] if imgs else None
    except Exception:
        return None

def placeholder_preview(text="Drag and drop a PDF above"):
    w, h = 860, 1000
    img = Image.new("RGB", (w, h), (248, 250, 252))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    try:
        bbox = d.textbbox((0, 0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    except AttributeError:
        tw, th = font.getsize(text)
    d.text(((w - tw) / 2, (h - th) / 2), text, fill=(107, 114, 128), font=font)
    st.image(img, use_column_width=True)

# ----------------------------- Page: Summarization -----------------------------
def page_summarization():
    header()

    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Drag and drop file here", type=["pdf"], help="Limit 200MB per file • PDF")
    st.caption("Limit 200MB per file • PDF")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    st.markdown("**🗨️ HEDIS AI Bot**", unsafe_allow_html=True)

    if "chat" not in st.session_state:
        st.session_state.chat = [{"role":"assistant","content":"Hello! How can I assist you?"}]

    for m in st.session_state.chat:
        cls = "assistant" if m["role"]=="assistant" else ""
        st.markdown(f"<div class='msg {cls}'><b>{'Hedis AI' if m['role']=='assistant' else 'You'}:</b> {m['content']}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        q = st.text_input(" ", placeholder="Is Linda compliant with ...", label_visibility="collapsed")
        sent = st.form_submit_button("Send")
    if sent and q.strip():
        st.session_state.chat.append({"role":"user","content":q.strip()})
        resp = "I'll check the extracted summaries and evidence to answer that. (Demo response)"
        st.session_state.chat.append({"role":"assistant","content":resp})

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    tabs = st.tabs(["Page Wise Summary", "Segmented Summary", "Conclusion"])
    with tabs[0]:
        st.markdown("<div class='soft'>Per-page bullets or highlights will appear here.</div>", unsafe_allow_html=True)
    with tabs[1]:
        st.markdown("<div class='soft'>Sectioned/segmented summary goes here.</div>", unsafe_allow_html=True)
    with tabs[2]:
        st.markdown("<div class='soft'>Final conclusion & compliance notes will appear here.</div>", unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([2, 1])
    with left:
        fname = uploaded.name if uploaded else "Linda_Test_Record_2420.pdf"
        st.markdown(f"**File Name:** {fname}")
    with right:
        page_num = st.number_input("Enter page number", min_value=1, value=1, step=1, key="sum_page")

    st.write("")
    if uploaded:
        data = uploaded.getvalue()
        img = render_pdf_page(data, int(page_num))
        if img is not None:
            st.image(img, use_column_width=True)
        else:
            st.info("Single-page preview requires `poppler`. Showing inline PDF instead.")
            embed_pdf(data, height=700)
    else:
        placeholder_preview()

# ----------------------------- Router -----------------------------
if page == "Summarization":
    page_summarization()
else:
    header()
    st.subheader(page)
    st.info("Placeholder page.")
