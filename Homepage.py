import streamlit as st

def show_homepage():
  st.set_page_config(page_title="Hospital Management System", page_icon="")
  st.markdown(get_gradient_style(), unsafe_allow_html=True)
  st.title("Welcome to the Hospital Management System")
  st.write("A comprehensive system for managing patients, doctors, and hospital operations.")


def get_gradient_style():
  """
  Defines the CSS style targeting the main app container.
  """
  return """
  <style>
    [data-testid="stAppViewContainer"] {
      background: linear-gradient(to bottom, #428bca, #337ab7);
    }

    [data-testid="stSidebar"] {
      background: linear-gradient(to bottom, #e0e7ff, #d1e0fc) !important;
    }
  </style>
  """


if __name__ == "__main__":
  # Call the homepage function
  show_homepage()