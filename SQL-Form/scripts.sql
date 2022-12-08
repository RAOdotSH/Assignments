-- To create a user and give the privileges.
CREATE USER 'rao'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'rao'@'localhost';
FLUSH PRIVILEGES;

-- Create the Database
CREATE DATABASE DBMS_Assignment;