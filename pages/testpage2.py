import streamlit as st
import mysql.connector
import datacred as dc
import pandas as pd


def staff_page():
    st.set_page_config(page_title="Staff page", page_icon="")
    st.title("Patient page")


    # Allow staff to add new patient (inside an expander)
    with st.expander("Add New Patient"):
        add_new_patient()

    st.write("Shows all the patients in the hospitals")
    # Display patient data
    display_patients_data()
    


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

    return pd.DataFrame(rows, columns=column_names)



def display_patients_data():
    df = mysqlconn()

    if not df.empty:
        st.title('Patients Data')
        st.write("Data from MySQL table 'Patients':")

        with st.expander("Search"):
            search_values = {}
            for column in df.columns:
                search_values[column] = st.text_input(f"Search {column}:", "")

        filtered_data = df.copy()
        for column, value in search_values.items():
            if value:
                filtered_data = filtered_data[filtered_data[column].str.contains(value, case=False)]

        filtered_data.reset_index(drop=True, inplace=True)
        st.dataframe(filtered_data)
    else:
        st.write("No data available from MySQL table 'Patients'")



def add_new_patient():
    name = st.text_input("Patient Name:")
    age = st.number_input("Age:")
    gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
    height = st.number_input("Height:")
    weight = st.number_input("Weight:")
    address = st.text_area("Address:")

    if st.button("Add Patient"):
        if name and age and gender and height and weight and address:
            insert_new_patient(name, age, gender, height, weight, address)
            st.success("Patient added successfully!")
        else:
            st.warning("Please fill in all fields.")



def insert_new_patient(name, age, gender, height, weight, address):
    try:
        connection = mysql.connector.connect(
            host=dc.host,
            user=dc.user,
            password=dc.password,
            database=dc.database,
            port=dc.port
        )

        cursor = connection.cursor()

        query = "INSERT INTO Patients (PatientName, Age, Gender, Height, Weight, Address) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (name, age, gender, height, weight, address)

        cursor.execute(query, data)
        connection.commit()

    except mysql.connector.Error as error:
        st.error(f"Failed to insert data into Patients table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    staff_page()
