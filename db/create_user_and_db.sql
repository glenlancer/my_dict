-- Simplify password policy.
-- These two seems not exsiting for newer version of mysql.
set global validate_password_policy=0;
set global validate_password_length=1;

-- Create user and database and grant privileges to the user.
create user 'dictuser'@'localhost' identified by 'dictuser123';
grant all privileges on `dict_db`.* to 'dictuser'@'localhost' identified by 'dictuser123';
flush privileges;
create database dict_db;
create database if not exists dict_db;

-- This one is used for exporting db to file or file to db.
-- But prefer to use mysqldump, since this one is harder to be configured.
grant file on *.* to 'dictuser'@'localhost';
