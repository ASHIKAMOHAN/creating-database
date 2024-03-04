import numpy as np
import pandas as pd
from faker import Faker
import sqlite3

# Initialize Faker to generate random data
fake = Faker()

# Number of patients and medical conditions
n_patients = 1000
n_conditions = 10

# Generate patient data
patients_data = {
    'PatientID': np.arange(1, n_patients + 1),
    'Name': [fake.name() for _ in range(n_patients)],
    'Age': np.random.randint(1, 100, size=n_patients),
    'Gender': np.random.choice(['Male', 'Female', 'Other'], size=n_patients),
    'BloodType': np.random.choice(['A', 'B', 'AB', 'O', None], size=n_patients),
    'Height_cm': np.random.normal(170, 10, n_patients),
    'Weight_kg': np.random.normal(70, 15, n_patients),
    'Postcode': [fake.postcode() for _ in range(n_patients)],
    'PatientKey': [fake.uuid4() for _ in range(n_patients)]
}
patients_df = pd.DataFrame(patients_data)

# Create duplicate values in specified columns
duplicate_columns = ['Name', 'Gender', 'BloodType']
for col in duplicate_columns:
    patients_df[col] = patients_df[col].sample(frac=1).reset_index(drop=True)

# Create an ordinal column for health status
health_status_categories = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
patients_df['Health_Status'] = np.random.choice(health_status_categories, size=n_patients)

# Define medical conditions
medical_conditions = [
    "Diabetes", "Hypertension", "Obesity", "Asthma", "Arthritis",
    "Cancer", "Heart Disease", "Depression", "Migraine", "Allergy"
]

# Generate medical conditions data
conditions_df = pd.DataFrame({
    'ConditionID': np.arange(1, n_conditions + 1),
    'Condition': np.random.choice(medical_conditions, size=n_conditions)
})

# Generate patient conditions data
patient_condition_data = {
    'PatientID': np.random.choice(patients_df['PatientID'], size=n_patients),
    'ConditionID': np.random.choice(conditions_df['ConditionID'], size=n_patients)
}
patient_conditions_df = pd.DataFrame(patient_condition_data)

# Generate appointment data
n_appointments = 2000  # Assuming multiple appointments per patient
appointment_data = {
    'AppointmentID': np.arange(1, n_appointments + 1),
    'PatientID': np.random.choice(patients_df['PatientID'], size=n_appointments),
    'Date': [fake.date_this_year() for _ in range(n_appointments)],
    'Time': [fake.time() for _ in range(n_appointments)]
}
appointments_df = pd.DataFrame(appointment_data)

# Save data to CSV files
patients_df.to_csv('patients.csv', index=False)
conditions_df.to_csv('medical_conditions.csv', index=False)
patient_conditions_df.to_csv('patient_conditions.csv', index=False)
appointments_df.to_csv('appointments.csv', index=False)

# Connect to SQLite database
conn = sqlite3.connect('patients_database.db')

# DataFrames to SQLite database tables
patients_df.to_sql('patients', conn, index=False, if_exists='replace')
conditions_df.to_sql('medical_conditions', conn, index=False, if_exists='replace')
patient_conditions_df.to_sql('patient_conditions', conn, index=False, if_exists='replace')
appointments_df.to_sql('appointments', conn, index=False, if_exists='replace')

# Adding constraints to the tables
conn.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        PatientID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Age INTEGER CHECK(Age > 0 AND Age < 150),
        Gender TEXT CHECK(Gender IN ('Male', 'Female', 'Other')),
        BloodType TEXT CHECK(BloodType IN ('A', 'B', 'AB', 'O', NULL)),
        Height_cm REAL CHECK(Height_cm > 0),
        Weight_kg REAL CHECK(Weight_kg > 0),
        Postcode TEXT,
        PatientKey TEXT UNIQUE
    );
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS medical_conditions (
        ConditionID INTEGER PRIMARY KEY,
        Condition TEXT NOT NULL UNIQUE
    );
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS patient_conditions (
        PatientID INTEGER,
        ConditionID INTEGER,
        PRIMARY KEY (PatientID, ConditionID),
        FOREIGN KEY (PatientID) REFERENCES patients(PatientID),
        FOREIGN KEY (ConditionID) REFERENCES medical_conditions(ConditionID)
    );
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        AppointmentID INTEGER PRIMARY KEY,
        PatientID INTEGER,
        Date TEXT,
        Time TEXT,
        FOREIGN KEY (PatientID) REFERENCES patients(PatientID)
    );
''')

# Commit changes and close connection
conn.commit()
conn.close()
