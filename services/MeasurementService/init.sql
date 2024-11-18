
CREATE USER 'user'@'%' IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

CREATE DATABASE IF NOT EXISTS bloodpressure;
USE bloodpressure;

CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_ssn VARCHAR(11) NOT NULL,
    systolic INT NOT NULL,
    diastolic INT NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (patient_ssn) REFERENCES patients(ssn)
);


FLUSH PRIVILEGES;
