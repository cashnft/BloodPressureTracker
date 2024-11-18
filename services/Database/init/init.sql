CREATE TABLE IF NOT EXISTS patients (
    ssn VARCHAR(11) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_ssn VARCHAR(11) NOT NULL,
    systolic INT NOT NULL,
    diastolic INT NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (patient_ssn) REFERENCES patients(ssn)
);