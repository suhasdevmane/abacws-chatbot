
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
docker exec --user="root" -it thingsbaord /bin/bash

copy conf file
docker cp bf52d15ee378:/etc/thingsboard/conf/thingsboard.yml ./thingsboard/          #replace container id

apt-get update
apt-get install vim
apt-get update -y
apt-get install -y iputils-pi
apt-get update && apt-get install -y iputils-ping


docker exec -it <CONTAINER ID/NAME>> env        # this wul 

docker exec -it <CONTAINER ID/NAME>> /bin/bash   # opens thingsboard@containerid:/$ psql

=============================
psql command line       


List all databases - \l
Switch to another database - \c <db-name>
List database tables - \dt
Describe a table - \d <table-name>
List all schemas - \dn
List users and their roles - \du
Retrieve a specific user - \du <username>
List all functions - \df 
List all views - \dv
Save query results to a file - \o <file-name>
see installed extension  -  \dx 
find available relations  - \d
Quit psql - \q




thingsboard=# SELECT * FROM device;             #lists all devices


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


copu files to change configuration

docker cp 82ef4aab77f1:/etc/thingsboard/conf/thingsboard.yml "C:/_PHD_/Github/abacws-chatbot/tb-pg-timescale/" 

pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=pgadmin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin

The default PostgreSQL user is thingsboard, changed password is Suhas@551993. 
Please, put your credentials here instead of default.


networking
read https://docs.docker.com/engine/tutorials/networkingcontainers/#:~:text=Docker%20networking%20allows%20you%20to,web%20app%20to%20the%20my_bridge%20.

a] Inspecting the network is an easy way to find out the container's IP address.
 docker network inspect bridge
b] remove a container from a network 
 docker network disconnect <network name -default is bridge> <container id or name >
c] Create your own bridge network
- A bridge network is limited to a single host running Docker Engine. An overlay network can include multiple hosts and is a more advanced topic. 
- For this example, create a bridge network:
 docker network create -d bridge <network name- e.g. my_bridge>    # -d flag tells Docker to use the bridge driver for the new network
d] list the networks
 docker network ls
e] Add containers to a network
docker run -d --net=my_bridge --name db training/postgres
docker run -d --net=my_bridge --name <container name lor id> <image>
f] If you inspect your my_bridge you can see it has a container attached. You can also inspect your container to see where it is connected:
 docker inspect --format='{{json .NetworkSettings.Networks}}'  db
g] get ip address of a container
 docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container name or id>









to look your ip address us : ipconfig 
and to know your containers ip address use : docker inspect <container_name>
-===================================================================
=================================================================
C:\_PHD_\Github\abacws-chatbot\thingsboard>docker exec -it timescale psql -U postgres   
psql (14.9)
Type "help" for help.

postgres=# \l
                                  List of databases
    Name     |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-------------+----------+----------+------------+------------+-----------------------
 example     | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres    | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
             |          |          |            |            | postgres=CTc/postgres
 template1   | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
             |          |          |            |            | postgres=CTc/postgres
 thingsboard | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
(5 rows)

postgres=# \c thingsboard 
You are now connected to database "thingsboard" as user "postgres".
thingsboard=# CREATE EXTENSION IF NOT EXISTS timescaledb;
NOTICE:  extension "timescaledb" already exists, skipping
CREATE EXTENSION
thingsboard=# psql -U postgres -h localhost thingsboard
thingsboard-# \dx
                                                List of installed extensions
    Name     | Version |   Schema   |                                      Description
-------------+---------+------------+--------------------------------------------------------------------------------------- 
 plpgsql     | 1.0     | pg_catalog | PL/pgSQL procedural language
 timescaledb | 2.12.0  | public     | Enables scalable inserts and complex queries for time-series data (Community Edition)  
(2 rows)


================================================================









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

docker exec -it timescaledb psql --version
timescaledb:
  image: timescale/timescaledb:2.5.0-pg14
  # Rest of your configuration...


Adjust JWT token expiry in thingsboard cnfiguration file.
```
docker exec -it <thingsboard container id>> /bin/bash
```

========================================= timescaledb ==============================

1. used image
  timescale:
    image: "timescale/timescaledb:latest-pg14"
    container_name: timescale
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=thingsboard
    ports:
      - "5433:5432"
    volumes:
      - timescaledb-data:/var/lib/postgresql/data
    command: ["-c", "shared_preload_libraries=timescaledb"]
    networks:
      - abacws-chatbot_my_bridge

networks:
  abacws-chatbot_my_bridge:
volumes:
  timescaledb-data:

  2. login into container psql 
     
     docker exec -it timescale psql -U postgres        <timescalle is a container name> <postgres is user>

  3. login to psql from any terminal command line
   
    psql -p 5433 -h localhost -U postgres        

  4. run query to see installed version of postgres 

    select version();

  5. create a database
  
     postgres=# create database thingsboard;

6. enter into the database

  postgres=# \c thingsboard

7. Create extension

 thingsboard=# CREATE EXTENSION IF NOT EXISTS timescaledb;

 8. List available extension in the database

  thingsboard=# \dx

