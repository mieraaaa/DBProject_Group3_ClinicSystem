DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS patient_phoneNumber;
DROP TABLE IF EXISTS doctor_phoneNumber;
DROP TABLE IF EXISTS doctor_clinic;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS clinic;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS doctor;

CREATE TABLE doctor
(
  doctorID INT NOT NULL,
  firstName VARCHAR(100) NOT NULL,
  lastName VARCHAR(100) NOT NULL,
  specialization VARCHAR(100) NOT NULL,
  PRIMARY KEY (doctorID)
);

CREATE TABLE patient
(
  patientID INT NOT NULL,
  firstName VARCHAR(100) NOT NULL,
  lastName VARCHAR(100) NOT NULL,
  emailAddress VARCHAR(255) NOT NULL,
  PRIMARY KEY (patientID)
);

CREATE TABLE clinic
(
  clinicID INTEGER PRIMARY KEY AUTOINCREMENT,
  clinicName VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  address VARCHAR(255) NOT NULL
);

CREATE TABLE room
(
  roomID INT NOT NULL,
  roomName VARCHAR(100) NOT NULL,
  capacity INT NOT NULL,
  clinicID INT NOT NULL,
  PRIMARY KEY (roomID),
  FOREIGN KEY (clinicID) REFERENCES clinic(clinicID)
);

CREATE TABLE doctor_clinic
(
  doctorID INT NOT NULL,
  clinicID INT NOT NULL,
  PRIMARY KEY (doctorID, clinicID),
  FOREIGN KEY (doctorID) REFERENCES doctor(doctorID),
  FOREIGN KEY (clinicID) REFERENCES clinic(clinicID)
);

CREATE TABLE doctor_phoneNumber
(
  phoneNumber VARCHAR(50) NOT NULL,
  doctorID INT NOT NULL,
  PRIMARY KEY (phoneNumber, doctorID),
  FOREIGN KEY (doctorID) REFERENCES doctor(doctorID)
);

CREATE TABLE patient_phoneNumber
(
  phoneNumber VARCHAR(50) NOT NULL,
  patientID INT NOT NULL,
  PRIMARY KEY (phoneNumber, patientID),
  FOREIGN KEY (patientID) REFERENCES patient(patientID)
);

CREATE TABLE appointment
(
  appointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE NOT NULL,
  time TIME NOT NULL,
  status VARCHAR(50) NOT NULL,
  patientID INT NOT NULL,
  doctorID INT NOT NULL,
  roomID INT NOT NULL,
  FOREIGN KEY (patientID) REFERENCES patient(patientID),
  FOREIGN KEY (doctorID) REFERENCES doctor(doctorID),
  FOREIGN KEY (roomID) REFERENCES room(roomID)
);