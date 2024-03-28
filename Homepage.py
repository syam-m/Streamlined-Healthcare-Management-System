import streamlit as st

def show_homepage():
  st.set_page_config(page_title="Hospital Management System", page_icon="")
  st.title("Welcome to the Hospital Management System")
  st.write("A comprehensive system for managing patients, doctors, and hospital operations.")


if __name__ == "__main__":
  # Call the homepage function
  show_homepage()