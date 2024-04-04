import streamlit as st
import mysql.connector
import datacred as dc
import pandas as pd

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
    column_names = [col[0] for col in cursor.description]  
    cursor.close()
    connection.close()

    if rows:
        st.title('Patients Data')
        st.write("Data from MySQL table 'Patients':")

        df = pd.DataFrame(rows, columns=column_names)

        with st.expander("Search"):
            # Allow users to search for a specific value in each column
            search_values = {}
            for column in df.columns:
                search_values[column] = st.text_input(f"Search {column}:", "")

        # Filter data based on search values
        filtered_data = df.copy()
        for column, value in search_values.items():
            if value:
                filtered_data = filtered_data[filtered_data[column].str.contains(value, case=False)]

        filtered_data.reset_index(drop=True, inplace=True)
        st.dataframe(filtered_data)
    else:
        st.write("No data available from MySQL table 'Patients'")


if __name__ == "__main__":
    staff_page()
