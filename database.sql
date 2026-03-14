CREATE DATABASE IF NOT EXISTS projeto_login;
USE projeto_login;
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255)
);