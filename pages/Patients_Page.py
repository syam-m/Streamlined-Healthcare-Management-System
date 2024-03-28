import streamlit as st
# import mysql.connector
# import os
# from src.pages.Datacred2 import host
from Datacred import host


def staff_page():
  st.set_page_config(page_title="Staff page", page_icon="")
  st.title("Staff page")
  st.write("Shows all the patients in the hospitals")
  st.write(host)

#   mysqlconn()



# def mysqlconn():
#     # Connect to MySQL database
#     connection = mysql.connector.connect(
#         host="your_host",
#         user="your_username",
#         password="your_password",
#         database="Final_project"
#     )

#     # Create a cursor object to execute queries
#     cursor = connection.cursor()

#     # Query data from the Patients table
#     cursor.execute("SELECT * FROM Patients")

#     # Fetch all rows from the result set
#     rows = cursor.fetchall()

#     # Close the cursor and connection
#     cursor.close()
#     connection.close()

#     # Display data in Streamlit
#     st.title('Patients Data')
#     st.write("Data from MySQL table 'Patients':")
#     st.write(rows)


if __name__ == "__main__":
  staff_page()