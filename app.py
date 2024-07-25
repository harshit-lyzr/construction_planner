from gptvision import GPTVISION
import streamlit as st
from PIL import Image
import utils
import base64
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Construction Planner",
    layout="wide",  # or "wide"
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

st.title("Construction Planner👷‍")


openai_4o_model = GPTVISION(api_key=api_key,parameters={})

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
def main():
    page = st.sidebar.radio("Navigation", ["Home", "Default", "Upload"])

    if page == "Home":
        st.markdown("## Welcome to the Construction Planner!")
        st.markdown(
            "In this App you need to Upload Your Construction map and It can generate Construction planning and Additional Consideration Like Material Management,Labor Management or etc.")
        st.markdown(f"""
                **How to get started**
                  \n-Upload an image
                  \n-Generate Construction Planning for your Construction Map
                its that easy!
                """)
        st.markdown(f"""
                ****How it works:****
                \n**1. Upload Construction Map:** Users upload a construction map in either PNG or JPG format. This map should contain detailed information, including dimensions and relevant construction details, for the best results.
                \n**2. Generate Planning:** The AI model uses the extracted details to generate a detailed planning outline, including weekly and monthly plans. It also considers additional aspects like material management, labor management, quality control, and budget management.
                \n**3. Display Results:** The generated construction plan is displayed on the application interface, providing users with a structured and comprehensive plan to follow.
                """)
        st.markdown("### Note: Upload Better Image with Dimensions and Other Details for better result. ")

    if page == "Default":
        st.sidebar.image("302182976_422201556643778_2409092908657518815_n.jpg")
        with st.spinner("Generating Construction Planning...."):
            encoded_image = encode_image("302182976_422201556643778_2409092908657518815_n.jpg")
            planning = openai_4o_model.generate_text(prompt=prompt, image_url=encoded_image)
            st.markdown(planning)

    if page == "Upload":
        uploaded_files = st.file_uploader("Upload Your Construction Map", type=['png', 'jpg'])
        if uploaded_files is not None:
                st.success(f"File uploaded: {uploaded_files.name}")
                st.sidebar.image(uploaded_files)
                file_path = utils.save_uploaded_file(uploaded_files)
                if file_path is not None:
                    with st.spinner("Generating Construction Planning...."):
                        encoded_image = encode_image(file_path)
                        planning = openai_4o_model.generate_text(prompt=prompt, image_url=encoded_image)
                        st.markdown(planning)

if __name__ == "__main__":
    main()

