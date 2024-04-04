import streamlit as st
import mysql.connector
import os
import datacred as dc


def staff_page():
  st.set_page_config(page_title="Staff page", page_icon="")
  st.title("Staff page")
  st.write("Shows all the patients in the hospitals")
  mysqlconn()


def mysqlconn():
    connection = mysql.connector.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Patients")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    st.title('Patients Data')
    st.write("Data from MySQL table 'Patients':")
    st.dataframe(rows) 


if __name__ == "__main__":
  staff_page()