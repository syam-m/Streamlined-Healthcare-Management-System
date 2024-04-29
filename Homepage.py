import streamlit as st
import base64


def show_homepage():
    st.set_page_config(page_title="Hospital Management System", page_icon="")
    st.markdown(get_gradient_style(image_path, image_width, image_height), unsafe_allow_html=True)


def get_gradient_style(image_path, image_width, image_height):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    return f"""
    <style>
      [data-testid="stAppViewContainer"] {{
        background-image: url('data:image/png;base64,{encoded_image}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
      }}

      [data-testid="stSidebar"] {{
        background: linear-gradient(to bottom, #e0e7ff, #d1e0fc) !important;
      }}
    </style>
    """



image_path = "images/Asset2.jpeg"

image_width = 1500
image_height = 750

if __name__ == "__main__":
    show_homepage()
