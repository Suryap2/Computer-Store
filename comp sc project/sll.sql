use quantum_bytes;

CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL
);

INSERT INTO User (email, firstName, password) 
VALUES ('gaganvk6@gmail.com', 'Gagan', 'Gagan123');

ALTER TABLE user
ADD COLUMN isAdmin TINYINT(1) DEFAULT 0;

select * from User;

create table products(
id int primary key auto_increment,
name varchar(50) NOT NULL,
description varchar(200),
price int,
image blob); 

select * from products;

insert into products(name, description, price)
values('Razor KeyBoard', 'Mechanical keyboard with customizable RGB lighting and responsive switches.', 5000),
('Razor Mouse', 'A high-performance gaming mouse with customizable buttons and precision sensors.', 4000),
('Razor Headphones', 'Comfortable gaming headphones with immersive sound and a noise-canceling microphone.', 8000),
('Razor Gaming Chair', 'Comfortable and supportive chair designed for long gaming sessions with adjustable features.', 30000),
('Razor Controller', 'Ergonomic game controller with programmable buttons and adjustable sensitivity.', 16000),
    ('Razor Webcam', 'High-definition webcam with crisp image quality and built-in microphone.', 10000),
    ('Razor Mousepad', 'Extended mouse pad with RGB lighting and a smooth surface for precise tracking.', 3000),
    ('Razor Laptop', 'Powerful gaming laptop with a sleek design and top-tier performance components.', 90000);