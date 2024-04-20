import streamlit as st
import pandas as pd



### Test 2

# def handle_delete_patient(patient_data):
#     for row in enumerate(patient_data):
#         if row[-1]:  # Check if the delete button for this row was clicked
#             delete_patient_record(row[0])  # Delete the record with the corresponding Patient_ID
#             st.success("Patient record deleted successfully!")
#             # Refetch and display updated patient data
#             updated_patient_data = fetch_patient_data()
#             display_patient_data(updated_patient_data)


# def handle_delete_patient(patient_data):
#     for row in patient_data:
#         if st.button(f"Delete "):  # Assign a unique key based on patient ID and name
#             delete_patient_record(row[0])  # Delete the record with the corresponding Patient_ID
#             st.success("Patient record deleted successfully!")
#             st.experimental_rerun()  # Refresh the page to reflect changes

### Test 2