--Run this to server to connect pc2
CREATE USER IF NOT EXISTS 'diet_app'@'192.168.0.127' IDENTIFIED BY 'Hakdog123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
ON `dietary_mgmt`.*
TO 'diet_app'@'192.168.0.127';
FLUSH PRIVILEGES;



--to BUILD
pyinstaller --clean --onefile --noconsole --icon ".\icon.ico" --collect-all mysql.connector .\inventory_app.py


--Check User
SELECT User, Host FROM mysql.user
WHERE User='diet_app';

DROP USER IF EXISTS 'diet_app'@'192.168.0.127';
DROP USER IF EXISTS 'diet_app'@'desktop-bnhi31o';
DROP USER IF EXISTS 'diet_app'@'desktop-v7l9hip';
DROP USER IF EXISTS 'diet_app'@'localhost';
DROP USER IF EXISTS 'diet_app'@'%';

-- Ensure the subnet user exists and has grants
CREATE USER IF NOT EXISTS 'diet_app'@'192.168.0.%' IDENTIFIED BY '';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
ON `dietary_mgmt`.*
TO 'diet_app'@'192.168.0.%';
FLUSH PRIVILEGES;

--worked
$env:DMS_DB_HOST="192.168.0.64"; $env:DMS_DB_PORT="3306"; $env:DMS_DB_USER="diet_app"; Remove-Item Env:\DMS_DB_PASSWORD -ErrorAction SilentlyContinue; $env:DMS_DB_NAME="dietary_mgmt"; & "D:\Dietary\Dietary Management System.exe"



--run this for connection
setx DMS_DB_HOST "192.168.0.64"
setx DMS_DB_PORT "3306"
setx DMS_DB_USER "diet_app"
setx DMS_DB_PASSWORD "Hakdog123!"
setx DMS_DB_NAME "dietary_mgmt"



--run this for databaswe setup (enter your pc 1 and pc2 ip address)
ALTER USER 'diet_app'@'192.168.0.64' IDENTIFIED BY 'Hakdog123!';
ALTER USER 'diet_app'@'192.168.0.177' IDENTIFIED BY 'Hakdog123!';   -- if this client should connect
DROP USER IF EXISTS 'diet_app'@'192.168.0.%';
DROP USER IF EXISTS 'diet_app'@'%';
DROP USER IF EXISTS 'diet_app'@'192.168.0.127';
DROP USER IF EXISTS 'diet_app'@'desktop-v7l9hip';
FLUSH PRIVILEGES;



--fix when the server pc cannot open 
CREATE USER IF NOT EXISTS 'diet_app'@'localhost' IDENTIFIED BY 'Hakdog123!';
-- If you also want to allow TCP localhost explicitly:
CREATE USER IF NOT EXISTS 'diet_app'@'127.0.0.1' IDENTIFIED BY 'Hakdog123!';

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
ON `dietary_mgmt`.*
TO 'diet_app'@'localhost';

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
ON `dietary_mgmt`.*
TO 'diet_app'@'127.0.0.1';

FLUSH PRIVILEGES;


--if with conflict with server pc using database use this
setx DMS_DB_HOST "127.0.0.1"
setx DMS_DB_PORT "3306"
setx DMS_DB_USER "diet_app"
setx DMS_DB_PASSWORD "Hakdog123!"
setx DMS_DB_NAME "dietary_mgmt"