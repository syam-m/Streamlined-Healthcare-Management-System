import psycopg2
import streamlit as st
import datacred as dc
import pandas as pd
from psycopg2 import IntegrityError



def get_gradient_style():
    """
    Defines the CSS style targeting the main app container.
    """
    return """
    <style>
      [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #e0e7ff, #d1e0fc);
      }

      [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #e0e7ff, #d1e0fc) !important;
      }
    </style>
    """


st.markdown(get_gradient_style(), unsafe_allow_html=True)

def doctors_page():
    st.title("Doctors Page")
    st.markdown(get_gradient_style(), unsafe_allow_html=True)

    # Form for adding new doctors
    st.header("Add New Doctor")
    doctor_name = st.text_input("Doctor Name")
    doctor_specialty = st.text_input("Doctor Specialty")
    departments = get_departments()
    doctor_department = st.selectbox("Doctor Department", departments)
    if st.button("Add Doctor"):
        if doctor_name and doctor_specialty and doctor_department:
            add_new_doctor(doctor_name, doctor_specialty, doctor_department)
        else:
            st.error("Please fill in all fields.")

    # Main content for searching doctors
    st.write("---")
    st.header("Search Doctors")

    # Text input for searching doctors by name
    search_name = st.text_input("Search Doctor by Name")
    if search_name:
        st.write(f"Search Results for '{search_name}':")
        search_results = search_doctors_by_name(search_name)
        if not search_results.empty:
            search_results['Selected'] = search_results.apply(lambda x: st.checkbox(f"Select {x['doctor_name']}", key=x['doctor_id']), axis=1)
            st.dataframe(search_results)
        else:
            st.write("No results found.")

    # Dropdown menu for selecting departments
    search_department = st.selectbox("Search Doctors by Department", [""] + departments)
    if search_department:
        st.write(f"Search Results for Doctors in '{search_department}' Department:")
        search_results = search_doctors_by_department(search_department)
        if not search_results.empty:
            search_results['Selected'] = search_results.apply(lambda x: st.checkbox(f"Select {x['doctor_name']}", key=x['doctor_id']), axis=1)
            st.dataframe(search_results)
        else:
            st.write("No results found.")

    # Delete selected doctors
    if st.button("Delete Selected Doctors"):
        selected_doctors = [row['doctor_id'] for index, row in search_results.iterrows() if row['Selected']]
        if selected_doctors:
            delete_doctor_and_update_visits(selected_doctors)
            st.success("Selected doctors deleted successfully!")
        else:
            st.warning("No doctors selected for deletion.")


def search_doctors_by_name(name):
    connection = psycopg2.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )
    query = f"SELECT * FROM doctors WHERE Doctor_Name LIKE '%{name}%'"
    data = pd.read_sql(query, connection)
    connection.close()
    return data


def search_doctors_by_department(department):
    connection = psycopg2.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )
    query = f"SELECT * FROM doctors WHERE Doctor_Department LIKE '%{department}%'"
    data = pd.read_sql(query, connection)
    connection.close()
    return data


def get_departments():
    connection = psycopg2.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )
    query = "SELECT DISTINCT Doctor_Department FROM doctors"
    departments = pd.read_sql(query, connection).iloc[:, 0].tolist()
    connection.close()
    return departments



def add_new_doctor(name, specialty, department):
    connection = psycopg2.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO doctors (Doctor_Name, Doctor_Specialty, Doctor_Department) VALUES (%s, %s, %s)",
                       (name, specialty, department))
        connection.commit()
        st.success("Doctor added successfully!")
    except IntegrityError as e:
        connection.rollback()
        st.error(f"Failed to add doctor. {e}")
    finally:
        connection.close()


def delete_doctor_and_update_visits(doctor_ids):
    connection = psycopg2.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )
    cursor = connection.cursor()
    try:
        # Update visits referencing the doctor to be deleted
        cursor.execute("UPDATE visits SET doctor_id = (SELECT doctor_id FROM doctors WHERE Doctor_Name = 'Dr. Temp') WHERE doctor_id IN %s", (tuple(doctor_ids),))
        
        # Delete the doctor
        cursor.execute("DELETE FROM doctors WHERE Doctor_ID IN %s", (tuple(doctor_ids),))
        
        connection.commit()
        st.success("Doctor deleted successfully!")
    except Exception as e:
        connection.rollback()
        st.error(f"Failed to delete doctor and update visits. {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    doctors_page()
