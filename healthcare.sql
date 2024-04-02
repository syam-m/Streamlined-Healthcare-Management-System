Create table healthcareData(
    Patient_ID varchar(5) Primary Key,
    FirstName varchar(25),
    Lastname varchar(25),
    FullName varchar(25),
    Date_of_Birth DATE,
    Visit_date DATE,
    Dcotor_ID varchar(4) NOT NULL,
    DoctorName varchar(25),
    Nurse_name varchar(25),
    Diagnosis varchar(255),
    Prescription varchar(200),
    Payment_amount int,
    Payment_menthod varchar(50),
    Room_number int,
    has_insurance int
)

select * from healthcareData