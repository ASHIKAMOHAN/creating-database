import numpy as np
import pandas as pd
from faker import Faker
import sqlite3

# Initialize Faker to generate random names
fake = Faker()

# Define number of patients and medical conditions
n_patients = 1000
n_conditions = 10

# Generate patient data
patients_data = {
    'PatientID': np.arange(1, n_patients + 1),
    'Name': [fake.name() for _ in range(n_patients)],
    'Age': np.random.randint(1, 100, size=n_patients),  # Ratio data
    # Nominal data with nulls
    'Gender': np.random.choice(['Male', 'Female', 'other'], size=n_patients),
    # Nominal data with nulls
    'BloodType': np.random.choice(['A', 'B', 'AB', 'O', None], size=n_patients),
    'Height_cm': np.random.normal(170, 10, n_patients),  # Interval data
    'Weight_kg': np.random.normal(70, 15, n_patients),  # Ratio data
    # Generating unique identifiers
    'PatientKey': [fake.uuid4() for _ in range(n_patients)]
}

# Duplicate some rows to create duplicates
patients_df = pd.DataFrame(patients_data)
# Concatenate 5% of the DataFrame to itself
patients_df = pd.concat([patients_df, patients_df.sample(frac=0.05)])

# Define  medical conditions
medical_conditions = [
    "Diabetes",
    "Hypertension",
    "Obesity",
    "Asthma",
    "Arthritis",
    "Cancer",
    "Heart Disease",
    "Depression",
    "Migraine",
    "Allergy",
]

# Generate medical conditions data
conditions_df = pd.DataFrame({
    'ConditionID': np.arange(1, n_conditions + 1),
    'Condition': np.random.choice(medical_conditions, size=n_conditions)
})

# Duplicate some rows to create duplicates
# Concatenate 5% of the DataFrame to itself
conditions_df = pd.concat([conditions_df, conditions_df.sample(frac=0.05)])

# Generate patient conditions data (many-to-many relationship)
patient_condition_data = {
    'PatientID': np.random.choice(patients_df['PatientID'], size=n_patients),
    'ConditionID': np.random.choice(conditions_df['ConditionID'], size=n_patients)
}

# Duplicate some rows to create duplicates
patient_conditions_df = pd.DataFrame(patient_condition_data)
patient_conditions_df = pd.concat([patient_conditions_df, patient_conditions_df.sample(
    frac=0.05)])  # Concatenate 5% of the DataFrame to itself

# Generate appointment data
n_appointments = 2000  # Assuming multiple appointments per patient
appointment_data = {
    'AppointmentID': np.arange(1, n_appointments + 1),
    'PatientID': np.random.choice(patients_df['PatientID'], size=n_appointments),
    # Interval data
    'Date': [fake.date_this_year() for _ in range(n_appointments)],
    'Time': [fake.time() for _ in range(n_appointments)]  # Interval data
}

# Duplicate some rows to create duplicates
appointments_df = pd.DataFrame(appointment_data)
# Concatenate 5% of the DataFrame to itself
appointments_df = pd.concat(
    [appointments_df, appointments_df.sample(frac=0.05)])

# Save data to CSV files
patients_df.to_csv('patients.csv', index=False)
conditions_df.to_csv('medical_conditions.csv', index=False)
patient_conditions_df.to_csv('patient_conditions.csv', index=False)
appointments_df.to_csv('appointments.csv', index=False)

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('patients_database.db')

# Write DataFrames to SQLite database tables
patients_df.to_sql('patients', conn, index=False, if_exists='replace')
conditions_df.to_sql('medical_conditions', conn,
                     index=False, if_exists='replace')
patient_conditions_df.to_sql(
    'patient_conditions', conn, index=False, if_exists='replace')
appointments_df.to_sql('appointments', conn, index=False, if_exists='replace')

# Commit changes and close connection
conn.commit()
conn.close()

# Function to read data from SQLite database into a DataFrame
def read_table_to_dataframe(database_file, table_name):
    """
    Reads data from a table in an SQLite database and returns a Pandas DataFrame.

    Parameters:
    - database_file (str): Path to the SQLite database file.
    - table_name (str): Name of the table to read from.

    Returns:
    - pandas.DataFrame: DataFrame containing the data from the specified table.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)

    # Read data from the specified table into a DataFrame
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    return df

# Example usage of the function to read patients data
patients_from_db = read_table_to_dataframe('patients_database.db', 'patients')
print(patients_from_db.head())
