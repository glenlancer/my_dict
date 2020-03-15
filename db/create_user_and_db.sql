-- Simplify password policy.
-- These two seems not exsiting for newer version of mysql.
set global validate_password_policy=0;
set global validate_password_length=1;

-- Create user and database and grant privileges to the user.
create user 'dictuser'@'localhost' identified by 'dictuser123';
create database dict_db;
grant all privileges on `dict_db`.* to 'dictuser'@'localhost' identified by 'dictuser123';
flush privileges;