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
  clinicID INT NOT NULL,
  clinicName VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  address VARCHAR(255) NOT NULL,
  PRIMARY KEY (clinicID)
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
  appointmentID INT NOT NULL,
  date DATE NOT NULL,
  time TIME NOT NULL,
  status VARCHAR(50) NOT NULL,
  patientID INT NOT NULL,
  doctorID INT NOT NULL,
  roomID INT NOT NULL,
  PRIMARY KEY (appointmentID),
  FOREIGN KEY (patientID) REFERENCES patient(patientID),
  FOREIGN KEY (doctorID) REFERENCES doctor(doctorID),
  FOREIGN KEY (roomID) REFERENCES room(roomID)
);
