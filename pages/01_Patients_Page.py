import streamlit as st 
import pandas as pd
import psycopg2
import datacred as dc

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
st.title("Patients")

conn = psycopg2.connect(
          host=dc.host,
          user=dc.user,
          password=dc.password,
          database=dc.database,
          port=dc.port
    )
cur = conn.cursor()

def fetch_patient_data():
    cur.execute("SELECT * FROM Patients")
    rows = cur.fetchall()
    # print(rows)
    return rows

def display_patient_data(patient_data):
    df = pd.DataFrame(patient_data, columns=["Patient ID", "First Name", "Last Name", "Age", "Gender", "Height", "Weight", "Allergies", "Address", "Insurance Provider"])
    st.dataframe(df)

def insert_patient_data(first_name, last_name, age, gender, height, weight, allergies, address, insurance_provider):
    cur.execute("INSERT INTO Patients (Patient_First_Name, Patient_Last_Name, Age, Gender, Height, Weight, Allergies, Address, Insurance_Provider) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, age, gender, height, weight, allergies, address, insurance_provider))
    conn.commit()
    st.success("Patient record added successfully!")

def display_patient_data_with_delete(patient_data):
    if patient_data:
        df = pd.DataFrame(patient_data, columns=["Patient ID", "First Name", "Last Name", "Age", "Gender", "Height", "Weight", "Allergies", "Address", "Insurance Provider"])
        
        df["Delete"] = df.apply(lambda row: st.checkbox("", value=False, key=f"delete_{row['Patient ID']}"), axis=1)
        
        st.dataframe(df)

        patient_ids_to_delete = [row["Patient ID"] for idx, row in df.iterrows() if row["Delete"]]
        

        if st.button("Delete Selected"):
            for patient_id in patient_ids_to_delete:
                delete_patient_record(patient_id)
            st.success("Selected patient records deleted successfully!")
    else:
        st.write("No matching patients found.")




def delete_patient_record(patient_id):
        cur.execute("DELETE FROM Patients WHERE Patient_ID = %s", (patient_id,))
        conn.commit()
        st.success("Patient record deleted successfully!")
    

def add_patient_form():
    st.subheader("Add New Patient")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", ["M", "F"])
    height = st.number_input("Height (cm)", min_value=0.0)
    weight = st.number_input("Weight (kg)", min_value=0.0)
    allergies = st.text_area("Allergies")
    address = st.text_area("Address")
    insurance_provider = st.text_input("Insurance Provider")
    if st.button("Add Patient"):
        insert_patient_data(first_name, last_name, age, gender, height, weight, allergies, address, insurance_provider)
    


def search_patients():
    st.subheader("Search Patients")
    search_term = st.text_input("Enter patient's first or last name:")

    if search_term:
        search_query = f"""
        SELECT * FROM Patients
        WHERE Patient_First_Name ILIKE '%{search_term}%' OR Patient_Last_Name ILIKE '%{search_term}%'
        """
        cur.execute(search_query)
        search_results = cur.fetchall()
        

        if search_results:
            st.write("Search Results:")
            display_patient_data_with_delete(search_results)

        else:
            st.write("No matching patients found.")
    else:

        fetch_patient_data()


def patient_profile():
    st.subheader("Patient Profile")

    patient_data = fetch_patient_data()
    

    if patient_data:

        df = pd.DataFrame(patient_data, columns=["Patient ID", "First Name", "Last Name", "Age", "Gender", "Height", "Weight", "Allergies", "Address", "Insurance Provider"])

        st.dataframe(df)
    else:
        st.write("No patient records found.")

page_selection = st.sidebar.radio("Navigation", ["Search Patients","Add Patient", "Patient Profile"])


if page_selection == "Search Patients":
    search_patients()
elif page_selection == "Add Patient":
    add_patient_form()  
elif page_selection == "Patient Profile":
    patient_profile()