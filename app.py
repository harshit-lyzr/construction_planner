from gptvision import GPTVISION
import streamlit as st
from PIL import Image
import utils
import base64
import os

st.set_page_config(
    page_title="Construction Planner",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Construction Planner👷‍")
st.sidebar.markdown("## Welcome to the Construction Planner!")
st.sidebar.markdown("In this App you need to Upload Your Construction map and It can generate Construction planning and Additional Consideration Like Material Management,Labor Management or etc.")

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE",type="password")

if api:
        openai_4o_model = GPTVISION(api_key=api,parameters={})
else:
        st.sidebar.error("Please Enter Your OPENAI API KEY")

data = "data"
os.makedirs(data, exist_ok=True)

def encode_image(image_path):
        with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')


prompt = f"""
You are an expert Construction Manager.Your Task Is to Create Outline and Planning Schedule Based on Given Construction Map.
1/ Analyze Construction map and Get all Necessary details to curate Planning
2/ Create Weekly Plan and Monthly plan.
3/ Create Additional Consideration like Materials,Labor Management,Quality Control And Budget Management.

Output Requirement:
Analysis of Construction Map:
Weekly Plans:
Monthly Plans:
Additional Consideration:
"""

uploaded_files = st.file_uploader("Upload Your Construction Map", type=['png', 'jpg'])
if uploaded_files is not None:
        st.success(f"File uploaded: {uploaded_files.name}")
        file_path = utils.save_uploaded_file(uploaded_files)
        if file_path is not None:
                encoded_image = encode_image(file_path)
                planning = openai_4o_model.generate_text(prompt=prompt, image_url=encoded_image)
                st.markdown(planning)



