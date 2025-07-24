
import pandas as pd
import psycopg2
from datetime import datetime

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="healthcare_db",
        user="postgres",
        password="your_password",  # Replace with your PostgreSQL password
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    print("Connected to PostgreSQL successfully")
except Exception as e:
    print(f"Failed to connect to PostgreSQL: {e}")
    exit()

# Load Kaggle dataset
try:
    df = pd.read_csv("healthcare_dataset.csv")
    # Clean column names: remove whitespace, convert to lowercase
    df.columns = [col.strip().lower() for col in df.columns]
    print("CSV columns:", df.columns.tolist())
except Exception as e:
    print(f"Failed to read CSV: {e}")
    cur.close()
    conn.close()
    exit()

# Step 1: Insert unique Hospitals
hospitals = df[['hospital']].drop_duplicates().reset_index(drop=True)
hospitals['hospitalid'] = range(1, len(hospitals) + 1)
hospitals_dict = dict(zip(hospitals['hospital'], hospitals['hospitalid']))
try:
    cur.executemany(
        "INSERT INTO Hospitals (HospitalID, Name, Location, Capacity) VALUES (%s, %s, %s, %s)",
        [(row['hospitalid'], row['hospital'], 'Unknown', 100) for _, row in hospitals.iterrows()]
    )
    print("Inserted Hospitals")
except Exception as e:
    print(f"Error inserting Hospitals: {e}")
    cur.close()
    conn.close()
    exit()

# Step 2: Insert unique Doctors
doctors = df[['doctor']].drop_duplicates().reset_index(drop=True)
doctors['doctorid'] = range(1, len(doctors) + 1)
doctors_dict = dict(zip(doctors['doctor'], doctors['doctorid']))
try:
    cur.executemany(
        "INSERT INTO Doctors (DoctorID, Name, Specialization, Contact) VALUES (%s, %s, %s, %s)",
        [(row['doctorid'], row['doctor'], 'Unknown', 'Unknown') for _, row in doctors.iterrows()]
    )
    print("Inserted Doctors")
except Exception as e:
    print(f"Error inserting Doctors: {e}")
    cur.close()
    conn.close()
    exit()

# Step 3: Insert Patients
patients = df[['name', 'age', 'gender', 'blood type', 'insurance provider']].drop_duplicates().reset_index(drop=True)
patients['patientid'] = range(1, len(patients) + 1)
patients_dict = dict(zip(patients['name'], patients['patientid']))
try:
    cur.executemany(
        "INSERT INTO Patients (PatientID, Name, Age, Gender, Contact, MedicalHistory) VALUES (%s, %s, %s, %s, %s, %s)",
        [(row['patientid'], row['name'], row['age'], row['gender'], 'Unknown', f"Blood Type: {row['blood type']}, Insurance: {row['insurance provider']}") for _, row in patients.iterrows()]
    )
    print("Inserted Patients")
except Exception as e:
    print(f"Error inserting Patients: {e}")
    cur.close()
    conn.close()
    exit()

# Step 4: Insert Appointments
appointments = df[['name', 'date of admission', 'admission type', 'hospital', 'doctor']].reset_index(drop=True)
appointments['appointmentid'] = range(1, len(appointments) + 1)
try:
    cur.executemany(
        "INSERT INTO Appointments (AppointmentID, PatientID, DoctorID, HospitalID, AppointmentDate, BookingDate, Status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        [(row['appointmentid'], patients_dict[row['name']], doctors_dict[row['doctor']], hospitals_dict[row['hospital']], row['date of admission'], row['date of admission'], row['admission type'] if row['admission type'] in ['Scheduled', 'Urgent'] else 'Urgent') for _, row in appointments.iterrows()]
    )
    print("Inserted Appointments")
except Exception as e:
    print(f"Error inserting Appointments: {e}")
    cur.close()
    conn.close()
    exit()

# Step 5: Insert MedicalRecords
medical_records = df[['name', 'medical condition', 'medication', 'test results', 'date of admission']].reset_index(drop=True)
medical_records['recordid'] = range(1, len(medical_records) + 1)
try:
    cur.executemany(
        "INSERT INTO MedicalRecords (RecordID, PatientID, Diagnosis, Treatment, Date, Prescription) VALUES (%s, %s, %s, %s, %s, %s)",
        [(row['recordid'], patients_dict[row['name']], row['medical condition'], f"Test Results: {row['test results']}", row['date of admission'], row['medication']) for _, row in medical_records.iterrows()]
    )
    print("Inserted MedicalRecords")
except Exception as e:
    print(f"Error inserting MedicalRecords: {e}")
    cur.close()
    conn.close()
    exit()

# Commit and close
conn.commit()
cur.close()
conn.close()
print("Kaggle dataset imported successfully!")
