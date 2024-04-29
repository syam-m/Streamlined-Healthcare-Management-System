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


def get_visit_details_by_record_id(record_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT V.Record_ID, P.Patient_First_Name, P.Patient_Last_Name, D.Doctor_Name, V.Symptoms, V.Tests, V.Diagnosis_Notes, V.Prescription
        FROM Visits V
        INNER JOIN Patients P ON V.Patient_ID = P.Patient_ID
        INNER JOIN Doctors D ON V.Doctor_ID = D.Doctor_ID
        WHERE V.Record_ID = %s
    """, (record_id,))
    visit_details = cursor.fetchone()
    cursor.close()
    return visit_details


def update_specific_visit_details(record_id, symptoms, tests, diagnosis_notes, prescription):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE Visits
            SET Symptoms = %s, Tests = %s, Diagnosis_Notes = %s, Prescription = %s
            WHERE Record_ID = %s
        """, (symptoms, tests, diagnosis_notes, prescription, record_id))
        connection.commit()
        st.success("Visit details updated successfully!")
    except Exception as e:
        connection.rollback()
        st.error(f"Error: {e}")
    finally:
        cursor.close()


def modify_specific_records():
    st.title("Modify Specific Records")


    record_id = st.text_input("Search Visit Record by Record ID")


    visit_details = None
    if record_id:
        visit_details = get_visit_details_by_record_id(record_id)
        if not visit_details:
            st.warning("No visit record found with the provided Record ID.")
        else:
            st.subheader("Visit Details")
            st.write(f"Record ID: {visit_details[0]}")
            st.write(f"Patient Name: {visit_details[1]} {visit_details[2]}")
            st.write(f"Doctor Name: {visit_details[3]}")


            st.subheader("Modify Specific Visit Details")
            symptoms = st.text_area("Symptoms", visit_details[4])
            tests = st.text_area("Tests", visit_details[5])
            diagnosis_notes = st.text_area("Diagnosis Notes", visit_details[6])
            prescription = st.text_area("Prescription", visit_details[7])


            if st.button("Update Specific Details"):
                update_specific_visit_details(record_id, symptoms, tests, diagnosis_notes, prescription)


if __name__ == "__main__":
    modify_specific_records()
