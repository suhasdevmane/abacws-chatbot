
REF - https://thingsboard.io/docs/user-guide/install/docker-windows/
Prerequisites
    : DOCKER DESKTOP

Running
Depending on the database used there are three type of ThingsBoard single instance docker images:

thingsboard/tb-postgres - single instance of ThingsBoard with PostgreSQL database.

Recommended option for small servers with at least 1GB of RAM and minimum load (few messages per second). 2-4GB is recommended.

thingsboard/tb-cassandra - single instance of ThingsBoard with Cassandra database.

The most performant and recommended option but requires at least 6GB of RAM. 8GB is recommended.

thingsboard/tb - single instance of ThingsBoard with embedded HSQLDB database.

Note: Not recommended for any evaluation or production usage and is used only for development purposes and automatic tests.



=============================
sysadmin- use default credentials
sysadmin@thingsboard.org / sysadmin
tenant@thingsboard.org / tenant
customer@thingsboard.org / customer

docker Thingsboard local
tenant- suhasdevmane@gmail.com
pass - Suhas@551993

docker compose up -d            #to up docker compose
docker compose down             # to stop docker-compose 
docker compose logs -f mytb    #to see logs
docker compose stop mytb
docker compose start mytb


lOGIN TO SHELL

docker exec --user="root" -it b9440731d41b /bin/bash
apt-get update
apt-get install vim

docker exec -it <CONTAINER ID/NAME>> env        # this wul 

docker exec -it <CONTAINER ID/NAME>> /bin/bash

=============================
psql command line

SELECT * FROM device;


thingsboard itself has postgress installed. 
default username - thingsboard
default password- postgres

default username - postgres         #NA
default password- postgres          #


to change postgress password inside the thingsboard-postgress use 
1. docker exec -it <container_name or id of thingsbaord/tb-postgress> bash 
2. psql 
3. show data_directory;
4. \password thingsboard    # to change password for user thingsboard
5. \q to exit psql




pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=pgadmin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin

The default PostgreSQL user is thingsboard, changed password is Suhas@551993. 
Please, put your credentials here instead of default.

to look your ip address us : ipconfig 
and to know your containers ip address use : docker inspect <container_name>

login succeeed if -
name: <any name you want>
host: host.docker.internal
database: postgres
user: postgres
password: postgres
PORT-5432



Device-01
device token- CFhCbxXIY5a7uYyII0v3
curl -v -X POST http://localhost:8080/api/v1/CFhCbxXIY5a7uYyII0v3/telemetry --header Content-Type:application/json --data "{temperature:25}"
mosquitto_pub -d -q 1 -h localhost -p 1883 -t v1/devices/me/telemetry -u CFhCbxXIY5a7uYyII0v3 -m "{temperature:23}"

Device-02-off
curl -v -X POST http://localhost:8080/api/v1/MyJExSz1fCxSyQLmaHxD/telemetry --header Content-Type:application/json --data "{temperature:25}"
mosquitto_pub -d -q 1 -h localhost -p 1883 -t v1/devices/me/telemetry -u MyJExSz1fCxSyQLmaHxD -m "{temperature:25}"


apache-jena-fuski-server 

connect fuseki server to the vs code
1. name- any display name
endpoint- http://localhost:3030/abacws-sensor-network/sparql
usrname- admin
password- Suhas@551993

=======================
timescaledb

docker exec -it timescaledb psql -U postgres        # to run psql from docker contaner
\q to exit psql

