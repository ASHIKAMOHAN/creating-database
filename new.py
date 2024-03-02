import numpy as np
import pandas as pd
from faker import Faker
import random
import datetime
import sqlite3

# Initialize Faker object
fake = Faker()

# Generate Patients
n_patients = 1000
patients_data = []
for _ in range(n_patients):
    patient_id = fake.unique.random_number(digits=6)
    name = fake.name()
    age = random.randint(1, 100)
    gender = random.choice(['Male', 'Female', 'Other'])
    patients_data.append((patient_id, name, age, gender))

patients_df = pd.DataFrame(patients_data, columns=['Patient_ID', 'Name', 'Age', 'Gender'])

# Generate Appointments
n_appointments = 2000
appointments_data = []
for _ in range(n_appointments):
    appointment_id = fake.unique.random_number(digits=6)
    patient_id = random.choice(patients_df['Patient_ID'])
    appointment_type = random.choice(['General', 'Specialist', 'Emergency'])
    appointment_date = fake.date_time_between(start_date='-1y', end_date='+1y').strftime('%Y-%m-%d %H:%M:%S')
    appointments_data.append((appointment_id, patient_id, appointment_type, appointment_date))

appointments_df = pd.DataFrame(appointments_data, columns=['Appointment_ID', 'Patient_ID', 'Appointment_Type', 'Appointment_Date'])

# Generate Doctors
n_doctors = 50
doctors_data = []
for _ in range(n_doctors):
    doctor_id = fake.unique.random_number(digits=6)
    name = fake.name()
    specialty = fake.random_element(elements=('Cardiology', 'Orthopedics', 'Pediatrics', 'Neurology'))
    doctors_data.append((doctor_id, name, specialty))

doctors_df = pd.DataFrame(doctors_data, columns=['Doctor_ID', 'Name', 'Specialty'])

# Save data to CSV files
patients_df.to_csv('patients.csv', index=False)
appointments_df.to_csv('appointments.csv', index=False)
doctors_df.to_csv('doctors.csv', index=False)

# Connect to SQLite database
conn = sqlite3.connect('hospital_database.db')
cursor = conn.cursor()

# Define CSV file paths
patients_csv = 'patients.csv'
appointments_csv = 'appointments.csv'
doctors_csv = 'doctors.csv'

# Read CSV files into Pandas DataFrames
patients_df = pd.read_csv(patients_csv)
appointments_df = pd.read_csv(appointments_csv)
doctors_df = pd.read_csv(doctors_csv)

# Save data into SQLite tables
patients_df.to_sql('Patients', conn, if_exists='append', index=False)
appointments_df.to_sql('Appointments', conn, if_exists='append', index=False)
doctors_df.to_sql('Doctors', conn, if_exists='append', index=False)

# Commit changes and close connection
conn.commit()
conn.close()