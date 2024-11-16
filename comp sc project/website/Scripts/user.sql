use quantum_bytes;

CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);

INSERT INTO User (email, firstName, password) 
VALUES ('gaganvk6@gmail.com', 'Gagan', 'Gagan123456');

select * from User;