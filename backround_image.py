import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load your local image and encode it
img = get_base64_of_bin_file("img1.jpg")

# CSS for background and sidebar
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-color: #fefbd8;
    background-image: url("https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-03.jpg");
    background-size: 180%;
    background-position: top-left;
    background-repeat: no-repeat;
    background-attachment: local;
}}

[data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}

[data-testid="stSidebar"] {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
}}
</style>
"""

# Apply CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Main app
st.title("Background Image Example")
st.write("This page has a custom background image!")

# Sidebar
st.sidebar.header("Sidebar")
st.sidebar.write("This is the sidebar content.")
