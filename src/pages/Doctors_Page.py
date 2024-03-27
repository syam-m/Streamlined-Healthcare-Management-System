import streamlit as st

def doctors_page():
  st.set_page_config(page_title="Staff page", page_icon="")
  st.title("Doctors Page")
  st.write("Shows all the doctors in the hospitals")

if __name__ == "__main__":
  doctors_page()