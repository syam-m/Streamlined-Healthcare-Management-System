import streamlit as st
import base64


def show_homepage():
    st.set_page_config(page_title="Hospital Management System", page_icon="")
    st.markdown(get_gradient_style(image_path, image_width, image_height), unsafe_allow_html=True)

    st.write("""
    <style>
        /* Center the title horizontally */
        .title-container {
            display: flex;
            justify-content: center;
        }
        /* Ensure the title stays on one line */
        .title-text {
            white-space: nowrap;
            color: #333333; /* Set font color to light gray */
        }
        /* Set font color of other text */
        .main-text {
            color: #333333; /* Set font color to light gray */
        }
    </style>
    """, unsafe_allow_html=True)

    st.write('<div class="title-container"><h1 class="title-text">Electronic health record system (EHRS)</h1></div>', unsafe_allow_html=True)

    st.write('<div class="main-text">Welcome to the Hospital Management System</div>', unsafe_allow_html=True)
    st.write('<div class="main-text">A comprehensive system for managing patients, doctors, and hospital operations.</div>', unsafe_allow_html=True)

    # Additional text
    st.write("""
    <div class="main-text">
    Electronic health record system (EHRS) has been widely adopted over the past decade in both inpatient and outpatient settings for different hospitals (Virginio & Ricarte, 2015). However, EHRS has also brought unforeseen errors and other unanticipated consequences that can present safety risks. These issues can range from data accuracy, standardization, data backup issues, data security and authentication. Additionally mid and small clinics often face problems with the costly EHRS and need a reliable yet simple solution. Our product aims to solve these issues and be compatible for future expansions and upgrades. The SHMS pointed to address categories of issues.
    - Patient Management: Create a unified platform to store, manage, and retrieve crucial patient information, including medical history, visit records, billing details, and insurance coverage.
    - Admin Management: Facilitate administrative processes such as appointment scheduling, room allocation, and staff assignment to optimize workflows and resource utilization.
    - Efficient Patient Care: Enable healthcare providers to quickly access comprehensive patient records, leading to more informed decision-making and better patient outcomes.
    - Data-Driven Insights: Establish a foundation for future analysis of healthcare trends, operational bottlenecks, and potential areas for process improvement.
    </div>
    """, unsafe_allow_html=True)

    


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




image_path = "images/Asset1.png"
# image_path = "images/adt1.jpg"
image_width = 1500
image_height = 750

if __name__ == "__main__":
    show_homepage()
