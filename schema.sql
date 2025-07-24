
-- Creating Patients table
CREATE TABLE Patients (
    PatientID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INTEGER CHECK (Age >= 0),
    Gender VARCHAR(10),
    Contact VARCHAR(50),
    MedicalHistory TEXT
);

-- Creating Doctors table
CREATE TABLE Doctors (
    DoctorID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(50),
    Contact VARCHAR(50)
);

-- Creating Hospitals table
CREATE TABLE Hospitals (
    HospitalID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100),
    Capacity INTEGER CHECK (Capacity >= 0)
);

-- Creating Appointments table
CREATE TABLE Appointments (
    AppointmentID SERIAL PRIMARY KEY,
    PatientID INTEGER REFERENCES Patients(PatientID),
    DoctorID INTEGER REFERENCES Doctors(DoctorID),
    HospitalID INTEGER REFERENCES Hospitals(HospitalID),
    AppointmentDate DATE NOT NULL,
    BookingDate DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Scheduled'
);

-- Creating MedicalRecords table
CREATE TABLE MedicalRecords (
    RecordID SERIAL PRIMARY KEY,
    PatientID INTEGER REFERENCES Patients(PatientID),
    Diagnosis VARCHAR(100),
    Treatment TEXT,
    Date DATE NOT NULL,
    Prescription TEXT
);

-- Creating indexes for optimization
CREATE INDEX idx_patientid ON MedicalRecords(PatientID);
CREATE INDEX idx_diagnosis ON MedicalRecords(Diagnosis);
CREATE INDEX idx_appointment_patientid ON Appointments(PatientID);
