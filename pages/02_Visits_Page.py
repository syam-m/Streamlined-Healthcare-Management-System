import psycopg2
import streamlit as st
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



connection = psycopg2.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )

# Function to insert visit details into Visits table
def insert_visit_details(patient_id, admission_type, visit_date, room_number, doctor_id, symptoms, tests, diagnosis_notes, prescription, payment_amount, payment_method, payment_invoice_number):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO Visits (Patient_ID, Admission_Type, Visit_Date, Room_Number, Doctor_ID, Symptoms, Tests, Diagnosis_Notes, Prescription, Payment_Amount, Payment_Method, Payment_Invoice_Number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING Record_ID
        """, (patient_id, admission_type, visit_date, room_number, doctor_id, symptoms, tests, diagnosis_notes, prescription, payment_amount, payment_method, payment_invoice_number))
        record_id = cursor.fetchone()[0]
        connection.commit()
        st.success("Visit details inserted successfully!")
        st.info(f"Record ID: {record_id}")
    except psycopg2.IntegrityError:
        connection.rollback()
        st.error("Error: Integrity constraint violation. Please check the entered IDs.")
    except Exception as e:
        connection.rollback()
        st.error(f"Error: {e}")
    finally:
        cursor.close()

# Function to get patient IDs, first names, and last names based on search
def get_patients_by_name(name):
    cursor = connection.cursor()
    cursor.execute("SELECT Patient_ID, Patient_First_Name, Patient_Last_Name FROM Patients WHERE LOWER(Patient_Last_Name) LIKE LOWER(%s) OR LOWER(Patient_First_Name) LIKE LOWER(%s)", ('%' + name + '%', '%' + name + '%'))
    patients = cursor.fetchall()
    cursor.close()
    return patients

# Get doctor IDs and names
def get_doctors():
    cursor = connection.cursor()
    cursor.execute("SELECT Doctor_ID, Doctor_Name FROM Doctors")
    doctors = cursor.fetchall()
    cursor.close()
    return doctors

# Streamlit page
def main():
    st.title("Enter Visit Details")

    # Input fields
    name = st.text_input("Search Patient by First or Last Name")
    patients = get_patients_by_name(name)
    patient_options = [f"{patient[0]} - {patient[1]} {patient[2]}" for patient in patients]
    
    if not patients:
        st.warning("No patients found. Please add new patient to data.")
    else:
        selected_patient_options = st.multiselect("Select Patient", patient_options, [])
        selected_patient_ids = [int(option.split(" - ")[0]) for option in selected_patient_options]

        admission_type = st.selectbox("Admission Type", ["Inpatient", "Outpatient"])
        visit_date = st.date_input("Visit Date")
        room_number = st.text_input("Room Number")
        doctors = get_doctors()
        doctor_names = [doctor[1] for doctor in doctors]
        selected_doctor_name = st.selectbox("Doctor Name", doctor_names)
        selected_doctor_id = doctors[doctor_names.index(selected_doctor_name)][0]
        symptoms = st.text_area("Symptoms")
        tests = st.text_area("Tests")
        diagnosis_notes = st.text_area("Diagnosis Notes")
        prescription = st.text_area("Prescription")
        payment_amount = st.number_input("Payment Amount", min_value=0.0)
        payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Insurance"])
        payment_invoice_number = st.text_input("Payment Invoice Number")

        # Button to submit
        if st.button("Submit"):
            if selected_patient_ids:
                for patient_id in selected_patient_ids:
                    insert_visit_details(patient_id, admission_type, visit_date, room_number, selected_doctor_id, symptoms, tests, diagnosis_notes, prescription, payment_amount, payment_method, payment_invoice_number)
            else:
                st.warning("Please select a patient before submitting.")

if __name__ == "__main__":
    main()
