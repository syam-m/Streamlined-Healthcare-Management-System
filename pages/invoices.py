import streamlit as st
import pandas as pd
import psycopg2 as pg
# import matplotlib.pyplot as plt
# import seaborn as sns

# Function to initialize database connection
def init_connection():
    return pg.connect(**st.secrets["postgres"])

# Function to run SQL queries
def run_query(query):
    with init_connection().cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# Display Invoice Data
def display_invoices():
    # Fetch invoice data from the database
    invoices_data = run_query("SELECT visit_id, visit_date, room_number, tests, payment_amount, payment_method FROM visits;")
    
    # Convert the fetched data into a Pandas DataFrame
    invoices_df = pd.DataFrame(invoices_data, columns=['visit_id', 'visit_date', 'room_number', 'tests', 'payment_amount', 'payment_method'])
    
    # Display the DataFrame as a table
    st.write("Invoice Data:", invoices_df)

    revenue()

def revenue():
    st.title("System Revenue")
    
    # Execute SQL query to calculate total revenue
    total_revenue = run_query("SELECT SUM(payment_amount) FROM Visits;")
    
    st.write(f"Total Revenue: ${total_revenue[0][0]:,.2f}")


# Filter and Search
def filter_and_search():
    st.subheader("Filter and Search Invoices")

    # Get user input for filtering
    invoice_status = st.selectbox("Select Payment Type:", ["Credit Card", "Insurance", "Cash", "Debit Card", "Medicare"])
    
    # Fetch filtered invoice data from the database
    if invoice_status == "Credit Card":
        invoices_data = run_query("SELECT patient_id, visit_date, room_number, tests FROM visits where payment_method = 'Credit Card' ;")
    elif invoice_status == "Debit Card":
        invoices_data = run_query("SELECT patient_id, visit_date, room_number, tests FROM visits where payment_method = 'Debit Card' ;")
    elif invoice_status == "Insurance":
        invoices_data = run_query("SELECT patient_id, visit_date, room_number, tests FROM visits where payment_method = 'Insurance' ;")
    elif invoice_status == "Cash":
        invoices_data = run_query("SELECT patient_id, visit_date, room_number, tests FROM visits where payment_method = 'Cash' ;")
    else:
        invoices_data = run_query("SELECT patient_id, visit_date, room_number, tests FROM visits where payment_method = 'Medicare' ;")   
  
    invoices_df_filtered = pd.DataFrame(invoices_data, columns=['patient_id', 'visit_date', 'room_number', 'tests'])
    
    # Display the filtered DataFrame as a table
    st.write("Filtered Invoices:", invoices_df_filtered)


# Generate New Invoices
def generate_new_invoice():
    st.subheader("Generate New Invoice")
    # Provide form fields for user input
    customer_name = st.text_input("Patient id:")
    room_number = st.number_input("Room Number:")
    amount = st.number_input("Amount:")
    payment_mode = st.selectbox("Status:", ["Credit Card", "Debit Card", "Insurance", "Cash", "Medicare"])
    
    # Generate invoice based on user input
    if st.button("Generate Invoice"):
        # Add new invoice to the database
        run_query(f"INSERT INTO visits(patient_id, visit_date, room_number, tests) VALUES ('{customer_name}', {amount}, '{payment_mode}', '{room_number}');")
        st.success("Invoice generated successfully!")


# Main function to run the Streamlit app
def main():
    st.title("Invoices Data")
    
    # Display navigation options
    navigation = st.sidebar.radio("Navigation", ["Display Invoices", "Filter and Search", "Generate New Invoice"])
    # Execute functionality based on user choice
    
    if navigation == "Display Invoices":
        display_invoices()
    elif navigation == "Filter and Search":
        filter_and_search()
    elif navigation == "Generate New Invoice":
        generate_new_invoice()

if __name__ == "__main__":
    main()
