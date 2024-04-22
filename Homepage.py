import streamlit as st

def show_homepage():
  st.set_page_config(page_title="Hospital Management System", page_icon="")
  st.markdown(get_gradient_style(image_path, image_width, image_height), unsafe_allow_html=True)

  #st.markdown(get_gradient_style(), unsafe_allow_html=True)
  st.title("Welcome to the Hospital Management System")
  st.write("A comprehensive system for managing patients, doctors, and hospital operations.")


import base64

def get_gradient_style(image_path, image_width, image_height):
    """
    Defines the CSS style targeting the main app container.
    """
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    
    return f"""
    <style>
      [data-testid="stAppViewContainer"] {{
        
        background-image: url('data:image/png;base64,{encoded_image}');
        background-size: {image_width}px {image_height}px;
        background-repeat: no-repeat;
        background-attachment: fixed;
      }}

      [data-testid="stSidebar"] {{
        background: linear-gradient(to bottom, #e0e7ff, #d1e0fc) !important;
      }}
    </style>
    """

image_path = "images/adt1.jpg"
image_width = 1500  # Adjust as needed
image_height = 750 # Adjust as needed



if __name__ == "__main__":
  # Call the homepage function
  show_homepage()