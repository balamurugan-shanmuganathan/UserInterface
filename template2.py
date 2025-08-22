# app.py
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="HEDISAbstractor.AI", layout="wide")

# ===================== Shared Styles / Header =====================
st.markdown(
    """
    <style>
    .block-container {padding-top: 6rem !important; padding-bottom: 2rem;}
    .app-header {
        position: sticky;
        top: 2.8rem;
        z-index: 999;
        background: linear-gradient(90deg, #ff6a00, #ff8e3c);
        color: white;
        border-radius: 0 0 12px 12px;
        padding: 12px 16px;
        margin: 0 -1rem 1rem -1rem;
        display:flex; align-items:center; justify-content:space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,.15);
    }
    .brand {font-weight: 800; font-size: 20px; letter-spacing:.2px}
    .brand small {opacity:.9; font-weight:600; margin-left:8px}
    .right-bar {display:flex; gap:10px; align-items:center}
    .pill {
        display:inline-flex; align-items:center; gap:8px;
        background: rgba(255,255,255,.18);
        padding:6px 10px; border-radius: 999px; font-weight:600;
    }
    .avatar {
        width:28px; height:28px; border-radius:50%;
        background:#fff; color:#ff6a00; font-weight:800;
        display:inline-flex; align-items:center; justify-content:center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def header():
    """Reusable app header"""
    st.markdown(
        """
        <div class="app-header">
          <div class="brand">Test Application <small>App</small></div>
          <div class="right-bar">
            <span class="pill">Deploy</span>
            <span class="pill"><span class="avatar">A</span> Hi, Bala</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ===================== Sidebar =====================
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["ReviewMember", "New File Intake", "Data Repository", "App Statistics", "Summarization"],
    index=0,
)
st.sidebar.markdown("### Navigation")
mode = st.sidebar.radio("Select a page:", ["Single Processing", "Batch Processing"], index=0)

# ===================== Sample Data =====================
member_profile = {
    "Member_id": "2420",
    "FileID": "Linda_Test_Record_2420.pdf",
    "Name": "Linda Stark",
    "DOB": "02/07/1964",
    "Gender": "Female",
    "LOB": "Commercial PPO",
}

bcs_details = pd.DataFrame(
    {
        "Attribute": [
            "Member_id", "FileID", "Name", "Mammogram", "Mammogram_page_No",
            "Mammogram_DOS", "Mammogram_DOS_page_No", "Bilateral_Mastectomy",
        ],
        "Value": [
            "2420", "Linda_Test_Record_2420.pdf", "Linda Stark", "Yes", "2",
            "05/28/2024", "2", "Yes",
        ],
    }
)

# ===================== Pages =====================
def page_review_member():
    header()
    st.subheader("Member Info and Measures Data")

    tabs = st.tabs(["Member Info", "BCS", "BPD", "CBP", "HBD", "EED", "CCS"])

    with tabs[0]:
        st.markdown("<div class='card soft'>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1])
        with c1:
            st.markdown("**Member ID**")
            st.write(member_profile["Member_id"])
            st.markdown("**Name**")
            st.write(member_profile["Name"])
        with c2:
            st.markdown("**Gender**")
            st.write(member_profile["Gender"])
            st.markdown("**DOB**")
            st.write(member_profile["DOB"])
        with c3:
            st.markdown("**LOB**")
            st.write(member_profile["LOB"])
            st.markdown("**File**")
            st.write(member_profile["FileID"])
        with c4:
            st.markdown("**Processing Mode**")
            st.write(mode)
            st.markdown("**Measurement Year**")
            st.write("2024")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- BCS tab ---
    with tabs[1]:
        top = st.columns([8, 1])
        with top[0]:
            st.markdown("**Disposition Status:** Exclusion: BCS - Bilateral Mastectomy")
            st.markdown("**Confidence Score:** 91.618%")
        with top[1]:
            with st.popover("ℹ️"):
                st.write("This section shows extracted rationale, confidence, and anchors for the BCS measure.")

        with st.expander("Details for BCS", expanded=True):
            st.dataframe(bcs_details, use_container_width=True, hide_index=True)

        st.markdown('<div class="footer-btns">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("Review Member")
        with col2:
            st.button("View Summary")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Other measures ---
    def measure_tab(name, status="Open Gap", conf=82.4):
        st.markdown(f"**Disposition Status:** {status}")
        st.markdown(f"**Confidence Score:** {conf:.3f}%")
        with st.expander(f"Details for {name}", expanded=True):
            df = pd.DataFrame(
                {
                    "Attribute": ["Member_id", "FileID", f"{name}_evidence", f"{name}_page_No"],
                    "Value": [member_profile["Member_id"], member_profile["FileID"], "—", "—"],
                }
            )
            st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('<div class="footer-btns">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("Review Member", key=f"rev_{name}")
        with col2:
            st.button("View Summary", key=f"sum_{name}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[2]:
        measure_tab("BPD", status="Compliant", conf=88.12)
    with tabs[3]:
        measure_tab("CBP", status="Open Gap", conf=76.44)
    with tabs[4]:
        measure_tab("HBD", status="Exclusion: Pregnancy", conf=89.03)
    with tabs[5]:
        measure_tab("EED", status="Open Gap", conf=80.17)
    with tabs[6]:
        measure_tab("CCS", status="Compliant", conf=92.51)

def placeholder_page(title):
    header()
    st.subheader(title)
    st.info("This section is a placeholder. Add your own widgets/data here.")

# ===================== Router =====================
if page == "ReviewMember":
    page_review_member()
elif page == "New File Intake":
    placeholder_page("New File Intake")
elif page == "Data Repository":
    placeholder_page("Data Repository")
elif page == "App Statistics":
    placeholder_page("App Statistics")
else:
    placeholder_page("Summarization")
