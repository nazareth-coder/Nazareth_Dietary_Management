--Run this to server to connect pc2
CREATE USER IF NOT EXISTS 'diet_app'@'192.168.0.127' IDENTIFIED BY 'Hakdog123';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
ON `dietary_mgmt`.*
TO 'diet_app'@'192.168.0.127';
FLUSH PRIVILEGES;



--to BUILD
pyinstaller --clean --onefile --noconsole --name "Dietary Management System" --icon ".\icon.ico" --add-data "icon.ico;." --collect-all mysql.connector .\inventory_app.py


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













---------------------------------------------------------------------
RUN THIS TO EVERY PC GOING TO CONNECT TO SERVER
setx DMS_DB_HOST "192.168.0.98"
setx DMS_DB_PORT "3306"
setx DMS_DB_USER "diet_app"
setx DMS_DB_PASSWORD "HAKDOG123!"
setx DMS_DB_NAME "dietary_mgmt"

AFTER RUNNING RUN THIS TO CHECK
echo $env:DMS_DB_HOST



CREATE USER IF NOT EXISTS 'diet_app'@'%' IDENTIFIED BY 'HAKDOG123!';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
  ON `dietary_mgmt`.*
  TO 'diet_app'@'%';
FLUSH PRIVILEGES;

USE THIS TO GRANT BOTH IP'S 
CREATE USER 'diet_app'@'192.168.x.client1' IDENTIFIED BY 'HAKDOG123!';
CREATE USER 'diet_app'@'192.168.x.client2' IDENTIFIED BY 'HAKDOG123!';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX ON `dietary_mgmt`.* TO 'diet_app'@'192.168.x.client1';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX ON `dietary_mgmt`.* TO 'diet_app'@'192.168.x.client2';
DROP USER 'diet_app'@'%';
FLUSH PRIVILEGES;


MORE DETAILED COMMAND
-- Create per-client users
CREATE USER IF NOT EXISTS 'diet_app'@'192.168.1.21' IDENTIFIED BY 'HAKDOG123!';
CREATE USER IF NOT EXISTS 'diet_app'@'192.168.1.22' IDENTIFIED BY 'HAKDOG123!';

-- (Optional) if you also run the app on the server itself:
CREATE USER IF NOT EXISTS 'diet_app'@'localhost' IDENTIFIED BY 'HAKDOG123!';
-- or, if the app on server connects via LAN IP:
CREATE USER IF NOT EXISTS 'diet_app'@'192.168.1.10' IDENTIFIED BY 'HAKDOG123!';

-- Grant least-privilege on the database
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
  ON `dietary_mgmt`.*
  TO 'diet_app'@'192.168.1.21';

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
  ON `dietary_mgmt`.*
  TO 'diet_app'@'192.168.1.22';

-- If you created localhost or server-IP user, grant it too:
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
  ON `dietary_mgmt`.*
  TO 'diet_app'@'localhost';

-- Remove the broad wildcard user only AFTER the per-IP users exist
DROP USER IF EXISTS 'diet_app'@'%';

FLUSH PRIVILEGES;



IF YOU RUN IT SERVER PC AND ANOTHER 1 PC
CREATE USER IF NOT EXISTS 'diet_app'@'192.168.' IDENTIFIED BY 'HAKDOG123!';
CREATE USER IF NOT EXISTS 'diet_app'@'localhost' IDENTIFIED BY 'HAKDOG123!';  -- or 'diet_app'@'192.168.1.10'
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX ON `dietary_mgmt`.* TO 'diet_app'@'192.168.1.21';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX ON `dietary_mgmt`.* TO 'diet_app'@'localhost';
DROP USER IF EXISTS 'diet_app'@'%';
FLUSH PRIVILEGES;



RUN THIS TO SERVER PC IF YOU"RE GOING TO OPEN THE APP THERE
setx DMS_DB_HOST "127.0.0.1"
setx DMS_DB_PORT "3306"
setx DMS_DB_USER "diet_app"
setx DMS_DB_PASSWORD "HAKDOG123!"
setx DMS_DB_NAME "dietary_mgmt"