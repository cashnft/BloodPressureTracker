CREATE USER 'user'@'%' IDENTIFIED BY 'password';


GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;


CREATE DATABASE IF NOT EXISTS bloodpressure;


USE bloodpressure;


CREATE TABLE IF NOT EXISTS patients (
    ssn VARCHAR(11) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


FLUSH PRIVILEGES;
