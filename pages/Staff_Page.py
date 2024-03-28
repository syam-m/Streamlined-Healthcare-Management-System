import streamlit as st



def staff_page():
  st.set_page_config(page_title="Staff page", page_icon="")
  st.title("Staff page")
  st.write("Shows all the patients in the hospitals")

if __name__ == "__main__":
  staff_page()