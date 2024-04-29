import streamlit as st
import pandas as pd
import psycopg2 as pg
import datacred as dc
import matplotlib.pyplot as plt
import seaborn as sns



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


def init_connection():
    conn = pg.connect(
        host=dc.host,
        user=dc.user,
        password=dc.password,
        database=dc.database,
        port=dc.port
    )
    return conn


def run_query(query):
    conn = init_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
    conn.close()
    return result



def display_invoices():

    invoices_data = run_query("SELECT patient_id, visit_id, visit_date, room_number, tests, payment_amount, payment_method FROM visits;")
    

    invoices_df = pd.DataFrame(invoices_data, columns=['patient_id', 'visit_id', 'visit_date', 'room_number', 'tests', 'payment_amount', 'payment_method'])
    

    st.write("Invoice Data:", invoices_df)

    revenue()

def revenue():
    st.title("System Revenue")
    

    total_revenue = run_query("SELECT SUM(payment_amount) FROM Visits;")
    
    st.write(f"Total Revenue: ${total_revenue[0][0]:,.2f}")



def display_highest_billing_department():

    billing_data = run_query("""
    SELECT d.Doctor_Department, SUM(v.Payment_Amount) AS Total_Billing_Amount
    FROM Doctors d INNER JOIN Visits v ON d.Doctor_ID = v.Doctor_ID
    GROUP BY d.Doctor_Department
    ORDER BY Total_Billing_Amount DESC
    LIMIT 5;
    """)
    

    billing_df = pd.DataFrame(billing_data, columns=['Department', 'Total Billing Amount'])


    st.write("Highest Billing Department:")
    st.write(billing_df)


    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Department', y='Total Billing Amount', data=billing_df, ax=ax)
    ax.set_title('Total Billing Amount by Department')
    ax.set_xlabel('Department')
    ax.set_ylabel('Total Billing Amount')
    st.pyplot(fig)




def filter_and_search():
    st.subheader("Filter and Search Invoices")


    invoice_status = st.selectbox("Select Payment Type:", ["Credit Card", "Insurance", "Cash", "Debit Card", "Medicare"])
    

    if invoice_status == "Credit Card":
        invoices_data = run_query("SELECT patient_id, visit_id, visit_date, room_number, tests, payment_amount FROM visits where payment_method = 'Credit Card' ;")
    elif invoice_status == "Debit Card":
        invoices_data = run_query("SELECT patient_id, visit_id, visit_date, room_number, tests, payment_amount FROM visits where payment_method = 'Debit Card' ;")
    elif invoice_status == "Insurance":
        invoices_data = run_query("SELECT patient_id, visit_id, visit_date, room_number, tests, payment_amount FROM visits where payment_method = 'Insurance' ;")
    elif invoice_status == "Cash":
        invoices_data = run_query("SELECT patient_id, visit_id, visit_date, room_number, tests, payment_amount FROM visits where payment_method = 'Cash' ;")
    else:
        invoices_data = run_query("SELECT patient_id, visit_id, visit_date, room_number, tests, payment_amount FROM visits where payment_method = 'Medicare' ;")   
  
    invoices_df_filtered = pd.DataFrame(invoices_data, columns=['patient_id','visit_id', 'visit_date', 'room_number', 'tests','payment_amount'])
    

    st.write("Filtered Invoices:", invoices_df_filtered)


def invoice_viz():

    invoices_data = run_query("SELECT patient_id, visit_date, payment_amount, payment_method FROM visits;")
    

    invoices_df = pd.DataFrame(invoices_data, columns=['patient_id', 'visit_date', 'payment_amount', 'payment_method'])
    

    st.subheader("Total Revenue Over Time")
    total_revenue_over_time = invoices_df.groupby('visit_date')['payment_amount'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=total_revenue_over_time.index, y=total_revenue_over_time.values, ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Total Revenue Over Time")
    st.pyplot(fig)


    st.subheader("Distribution of Invoices by Payment Method")
    payment_method_distribution = invoices_df['payment_method'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    payment_method_distribution.plot(kind='bar', ax=ax)
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Number of Invoices")
    ax.set_title("Distribution of Invoices by Payment Method")
    st.pyplot(fig)



def display_common_admission_types():

    admission_data = run_query("""
    SELECT Admission_Type, COUNT(*) AS Count
    FROM Visits
    GROUP BY Admission_Type
    ORDER BY Count DESC;
    """)
    

    admission_df = pd.DataFrame(admission_data, columns=['Admission Type', 'Count'])


    st.write("Most Common Admission Types:")
    st.write(admission_df)


    fig, ax = plt.subplots()
    sns.barplot(x='Admission Type', y='Count', data=admission_df, ax=ax)
    ax.set_title('Most Common Admission Types')
    ax.set_xlabel('Admission Type')
    ax.set_ylabel('Count')
    st.pyplot(fig)



def display_patient_age_distribution():

    age_data = run_query("""
    SELECT Age
    FROM Patients;
    """)
    

    age_df = pd.DataFrame(age_data, columns=['Age'])


    st.write("Distribution of Patient Ages:")
    st.write(age_df.describe())


    fig, ax = plt.subplots()
    sns.histplot(data=age_df, x='Age', bins=10, ax=ax)
    ax.set_title('Distribution of Patient Ages')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)




def display_most_used_insurance_providers():

    insurance_data = run_query("""
    SELECT Insurance_Provider, COUNT(*) AS Count
    FROM Patients
    WHERE Insurance_Provider IS NOT NULL
    GROUP BY Insurance_Provider
    ORDER BY Count DESC;
    """)
    

    insurance_df = pd.DataFrame(insurance_data, columns=['Insurance Provider', 'Count'])


    st.write("Most Used Insurance Providers:")
    st.write(insurance_df)


    fig, ax = plt.subplots()
    sns.barplot(x='Insurance Provider', y='Count', data=insurance_df, ax=ax)
    ax.set_title('Most Used Insurance Providers')
    ax.set_xlabel('Insurance Provider')
    ax.set_ylabel('Count')
    ax.tick_params(axis='x', rotation=45)  
    st.pyplot(fig)





def main():
    st.title("Invoices Data")
        

    navigation = st.sidebar.radio("Navigation", ["Display Invoices", "Filter and Search", "Analysis"])

    
    if navigation == "Display Invoices":
        display_invoices()
        display_highest_billing_department()

    elif navigation == "Filter and Search":
        filter_and_search()
    elif navigation == "Analysis":
        invoice_viz()


        display_common_admission_types()

        display_patient_age_distribution()

        display_most_used_insurance_providers()


if __name__ == "__main__":
    main()
