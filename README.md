This project is under development.




Create a python virtual environment to access different APIs.
```
python -m venv ./abacws-chatbot-venv
```
to activate environment
```
./abacwsenvs/Scripts/activate
c:/_PHD_/Github/abacws-chatbot/abacws-chatbot-venv/Scripts/activate.bat
```

Upgrade pip
```
 python.exe -m pip install --upgrade pip
```

Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm



# Abacws Data Visualiser
Web application made to visualise IoT data for devices in the Abacws building at Cardiff University.\
This repository contains the API and the Visualiser tool, both of which are deployed using [docker](https://www.docker.com/).

Production deployments for these tools can be found at the following locations:
- [API](https://abacws.ggrainger.uk/api/)
- [Visualiser](https://abacws.ggrainger.uk/)

## Docs
You can view the documentation for the two separate services in their respective README files.
- [API](./api/README.md)
- [Visualiser](./visualiser/README.md)

## Docker compose
I recommend using docker compose to deploy this to your own server alongside [traefik](https://traefik.io/traefik/).\
An example compose file can be seen below.

```yml
version: '3.8'
services:
  mongo:
    image: mongo
    container_name: abacws-mongo
    restart: always
    volumes:
      - ./mongo:/data/db

  api:
    image: ghcr.io/randomman552/abacws-data-vis:api-latest
    container_name: abacws-api
    restart: always
    depends_on:
      - mongo

  visualiser:
    image: ghcr.io/randomman552/abacws-data-vis:visualiser-latest
    container_name: abacws-visualiser
    restart: always
    depends_on:
      - api
    # Traefik is recommended, you can set up a NGINX or Apache proxy instead, but traefik is much easier.
    labels:
      - "traefik.enable=true"
      - "traefik.http.services.abacws-visualiser.loadbalancer.server.port=80"
      - "traefik.http.routers.abacws-visualiser.rule=Host(`visualiser.abacws.example.com`)"
      - "traefik.http.routers.abacws-visualiser.entrypoints=https"
      - "traefik.http.routers.abacws-visualiser.tls=true"
```

## Supported tags
| Tag                 | Description                 |
|:-------------------:|:---------------------------:|
| `visualiser-latest` | Production ready visualiser |
| `visualiser-main`   | Development visualiser      |
| `visualiser-vx.y.z`  | Specific visualiser version |
| `api-latest`        | Production ready API        |
| `api-main`          | Development API             |
| `api-vx.y.z`         | Specific API version        |



 # thingsboard/tb-postgres
 ThingsBoard is an open-source IoT platform for data collection, processing, visualization, and device management.

Before starting Docker container run following commands to create a directory for storing data and logs and then change its owner to docker container user, to be able to change user, chown command is used, which requires sudo permissions (command will request password for a sudo access):
```
$ mkdir -p ~/.mytb-data && sudo chown -R 799:799 ~/.mytb-data
$ mkdir -p ~/.mytb-logs && sudo chown -R 799:799 ~/.mytb-logs
```
Execute the following command to run this docker directly:

$ docker run -it -p 9090:9090 -p 1883:1883 -p 7070:7070 -p 5683-5688:5683-5688/udp -v ~/.mytb-data:/data -v ~/.mytb-logs:/var/log/thingsboard --name mytb --restart always thingsboard/tb-postgres

Where:
```
docker run - run this container
-it - attach a terminal session with current ThingsBoard process output
-p 9090:9090 - connect local port 9090 to exposed internal HTTP port 9090
-p 1883:1883 - connect local port 1883 to exposed internal MQTT port 1883
-p 7070:7070 - connect local port 7070 to exposed internal Edge RPC port 7070
-p 5683-5688:5683-5688/udp - connect local UDP ports 5683-5688 to exposed internal COAP and LwM2M ports
-v ~/.mytb-data:/data - mounts the host's dir ~/.mytb-data to ThingsBoard DataBase data directory
v ~/.mytb-logs:/var/log/thingsboard - mounts the host’s dir ~/.mytb-data to ThingsBoard logs directory
--name mytb - friendly local name of this machine
--restart always - automatically start ThingsBoard in case of system reboot and restart in case of failure.
thingsboard/tb-postgres - docker image
```

After executing this command you can open http://{yor-host-ip}:9090 in your browser. You should see ThingsBoard login page. Use the following default credentials:
```
Systen Administrator: sysadmin@thingsboard.org / sysadmin
Tenant Administrator: tenant@thingsboard.org / tenant
Customer User: customer@thingsboard.org / customer
You can always change passwords for each account in account profile page.

```
## Add your data to the thingsboard devices to talk to the building in natural language and receive data from the database.

All API's and Services are available in following ports:

8090 : Abacws 3D Live visulisation.\
8090/api/ : Abacws 3D backend data API to perform queries.\
8080 : IoT sensor data platform, Thingsboard GUI.\
8080/swagger-ui/ : Thingsboard data query API for all devices and sensors.\
5050 :  PgAdmin GUI to connect thingsboard PostgreSQL database.\
3030 : Apache Jena Fusuki Server to host PDF data and to perform queries.\
5005 :  Rasa Server Host.\
5055 : Rasa Action Server Host.\
8082 : Access Rasa Chatbot WEB UI to talk to the abacws.


to access all API and Services, attach all container with a same network. You can create a network using command 
``` 
docker network create <network_name>
```
For example. I have used network called 'Network abacws-chatbot_my_bridge' in docker-compose file.

To Run All containers run :
```
docker compose up -d 
```
To inspect IP addresses assigned to your containers run: 
```
docker network inspect your_network_name

e.g. docker network inspect abacws-chatbot_my_bridge
```
To extract the container IDs from the JSON output, ru :
```
docker network inspect your_network_name | jq -r '.[0].Containers | keys[]'
docker network inspect abacws-chatbot_my_bridge | jq -r '.[0].Containers | keys[]'

```
For windows,  run :
```
FOR /f "tokens=*" %i IN ('docker ps -q') DO docker inspect -f "{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" %i
```

To see Containier ID , their anmes and network connected, run :
```
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Networks}}"

```



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
# Thingsboard Credentials

sysadmin- use default credentials
id- sysadmin@thingsboard.org / pass- sysadmin
id- tenant@thingsboard.org / pass-  tenant
id- customer@thingsboard.org / pass- customer


docker compose up -d            #to up docker compose
docker compose down             # to stop docker-compose 
docker compose logs -f mytb    #to see logs
docker compose stop mytb
docker compose start mytb

docker volumes are saved at \\wsl.localhost\docker-desktop-data\data\docker\volumes\mytb-data\_data\db

windows 11- \\wsl.localhost\docker-desktop-data\data\docker\volumes
ref - https://www.jianshu.com/p/9f2cd43098bb
===========================

# lOGIN TO SHELL
login to the docker container as a root usser to make changes. Use the docker conytainer id to wnter inside the docker.
```
docker exec --user="root" -it b9440731d41b /bin/bash
docker exec --user="root" -it thingsbaord /bin/bash
```
to copy the configuration file from the docker container to the local repository use cp commandfor example 
```
copy conf file
docker cp bf52d15ee378:/etc/thingsboard/conf/thingsboard.yml ./thingsboard/          #replace container id
```
to install required packages to make changes install necessory packages after accessing the container as room user

vim /var/lib/docker/containers/6b88c0c9d4a6a7c290c976265b0357187d69a572402b5889ea7d501fbbcf5da1/hostconfig.json

ref：https://www.jianshu.com/p/9f2cd43098bb

apt-get update
apt-get install vim
apt-get update -y
apt-get install -y iputils-pi
apt-get update && apt-get install -y iputils-ping

```
to see the different files inside the container use command 
```
docker exec -it <CONTAINER ID/NAME>> env        # this wul 

docker exec -it <CONTAINER ID/NAME>> /bin/bash   # opens thingsboard@containerid:/$ psql
```
=============================

# psql command line       

once you enter to the spql command line tool inside the docker container, you use following spql command to explore the postgresql database.
```
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
```
to the the list of available devices inside the thingsboard dtabase use
```
thingsboard=# SELECT * FROM device;             #lists all devices
```


thingsboard itself has postgress installed. the defaults are follows 
- Maintenance database - thingsboard
- default username - thingsboard
- default password- postgres
- hostname - host.docker.internal
you should change the passwords.
      



To change postgress password inside the thingsboard-postgress use 
```postgresdefault
1. docker exec -it <container_name or id of thingsbaord/tb-postgress> bash 
2. psql 
3. show data_directory;
4. \password thingsboard    # to change password for user thingsboard
5. \q to exit psql
```

copy files from the container to the local repository, to change configuration
```
docker cp 82ef4aab77f1:/etc/thingsboard/conf/thingsboard.yml "C:/_PHD_/Github/abacws-chatbot/tb-pg-timescale/" 
```docker cp f5adf293b941:/etc/postgresql/12/main/postgresql.conf "C:/_PHD_/Github/abacws-chatbot/"
Some configurations are need to be changed or should be passed in the docker-compose file.
```
pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=pgadmin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
```

<!-- ====================================== adminer and pgadmin ========================= -->


use system- postgreSQL
Server-mytb
Username- thingsboard
password-  postgres
database- thingsboard

result-
id- uuid
cretaed time - bigint
etc



<!-- ========================================= -->



networking
read https://docs.docker.com/engine/tutorials/networkingcontainers/#:~:text=Docker%20networking%20allows%20you%20to,web%20app%20to%20the%20my_bridge%20.

a] Inspecting the network is an easy way to find out the container's IP address.
```
 docker network inspect bridge
```
b] remove a container from a network 
 ```
 docker network disconnect <network name -default is bridge> <container id or name >
 ```
c] Create your own bridge network
- A bridge network is limited to a single host running Docker Engine. An overlay network can include multiple hosts and is a more advanced topic. 
- For this example, create a bridge network:
 ```
 docker network create -d bridge <network name- e.g. my_bridge>    # -d flag tells Docker to use the bridge driver for the new network
```
d] list the networks
 ```
 docker network ls
 ```
e] Add containers to a network
``` 
docker run -d --net=my_bridge --name db training/postgres
docker run -d --net=my_bridge --name <container name lor id> <image>
```
f] If you inspect your my_bridge you can see it has a container attached. You can also inspect your container to see where it is connected:
 ```
 docker inspect --format='{{json .NetworkSettings.Networks}}'  db
```
g] get ip address of a container
 ```
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container name or id>
```


To look your ip address use simple command
```
ipconfig
``` 
and to know your containers ip address use 
``` 
docker inspect <container_name>
```

To adjust the memory usage of docker , in windows add the configuration in the location C:\Users\c21054458\.wslconfig file and restart docker desktop. 
-===================================================================
=================================================================
My output looks as follows: 

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



Node_5.01
device token- bW9z8pFxLGQWmmRauup6
curl -v -X POST http://localhost:8080/api/v1/bW9z8pFxLGQWmmRauup6/telemetry --header Content-Type:application/json --data "{temperature:25}"
mosquitto_pub -d -q 1 -h host.docker.internal -p 1883 -t v1/devices/me/telemetry -u bW9z8pFxLGQWmmRauup6 -m "{temperature:25}"
mosquitto_pub -d -q 1 -h 192.168.1.85 -p 1883 -t v1/devices/me/telemetry -u bW9z8pFxLGQWmmRauup6 -m "{temperature:25}"
10.10.212.208

Node_5.02
device token - IUj42BykCyPsRoq17HqY
curl -v -X POST http://localhost:8080/api/v1/IUj42BykCyPsRoq17HqY/telemetry --header Content-Type:application/json --data "{temperature:25}"
mosquitto_pub -d -q 1 -h host.docker.internal -p 1883 -t v1/devices/me/telemetry -u IUj42BykCyPsRoq17HqY -m "{temperature:25}"

Do not forget to add firewall rule to accept the incoming traffic from outside ip to port 1883. in windows add a inbound rule to accept the traffic to port 1883 in firewall settings. follow instruction https://www.youtube.com/watch?v=GBUVyu69Qsk
=======================

# apache-jena-fuski-server 

connect fuseki server to the vs code
1. name- any display name
endpoint- http://localhost:3030/abacws-sensor-network/sparql
usrname- admin
password- Suhas@551993

=======================
# Timescaledb

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
    docker exec -it 26d02ee6c574 psql -U thingsboard  <thingsboard is User>

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



  # This project is maintained by Suhas **** and under the PhD research project.







To Create a image of the API for 3d Visulisation in github, comment 'build-api' triggers the build process of API using github actions. \
To Create a image of the visuliser for 3d Visulisation in github, comment 'build-visualiser' triggers the build process of visuliser using github actions. 


Owner: Suhas\
Contact: will be provided



or build custom api
// docker cp api\src\api\data\devices.json :/api/api/data/devices.json

my ARCCA host
username - ubuntu
key - abacws-smart-building.pem


to add git/la/hub files
cd existing_repo
git remote add origin https://gitlab.com/IOTGarage/talking-buildings.git
git branch -M main
git push -uf origin main
                                                                      
for gitlab :
git commit -m "initial commit"
git status
git push -uf origin main
git config --global user.name "devmanesp1@cardiff.ac.uk"
git config --global user.email "devmanesp1@cardiff.ac.uk"
git config --global --list
>git status
git remote show origin
>git push origin main
git pull
git branch --set-upstream-to=origin/main main                      #use to set your origin to main as default
git pull --allow-unrelated-histories
git pull
git push origin main




curl -X 'PUT' 'http://localhost:8090/api/devices/node_5.05/data' -H 'accept: */*' -H 'Content-Type: application/json' -d '{ "temperature": {"value": 21, units": °C"}}'




Hosting Abacws 3d tool on ARCCA
TO SHOW NETWORKS USE=>  nmcli -p device show

to check public ip address => curl ifconfig.me     or wget -qO- ifconfig.me

ssh -i ".ssh/abacws-smat-building.pem" ubuntu@abaces-smart-building.arcca.cloud
10.0.3.48
172.17.0.1
172.18.0.1

ssh -i ".ssh/abacws-visualizer.pem" ubuntu@abacws-visualizer.arcca.cloud
10.0.3.45 172.19.0.1 172.17.0.1

https://7465-3-252-98-203.ngrok.io


curl -s https://checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'  
dig +short myip.opendns.com @resolver1.opendns.com      3.252.98.203
$ host myip.opendns.com resolver1.opendns.com | grep "myip.opendns.com has" | awk '{print $4}'
 wget -qO- http://ipecho.net/plain | xargs echo

 ngrok http 8080

  docker run -it -e NGROK_AUTHTOKEN=2XzP2J1VpPiGZlzfOf2igFdIjhh_hg4kYbuU19h1UaoaSp8v ngrok/ngrok http 8080
  ngrok config add-authtoken 2XzP2J1VpPiGZlzfOf2igFdIjhh_hg4kYbuU19h1UaoaSp8v  

   https://6320-34-254-240-101.ngrok-free.app

   sudo socat TCP-LISTEN:80,fork TCP:localhost:80


<!-- ========================= installiing timescaleDB ============================= -->

reference- https://docs.timescale.com/self-hosted/latest/install/installation-linux/

1. docker exec --user="root" -it <container id> /bin/bash
2. apt install gnupg postgresql-common apt-transport-https lsb-release wget
3. /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
4. echo "deb https://packagecloud.io/timescale/timescaledb/debian/ $(lsb_release -c -s) main" | tee /etc/apt/sources.list.d/timescaledb.list 

or
4. echo "deb https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -c -s) main" | tee /etc/apt/sources.list.d/timescaledb.list
5. wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | apt-key add -
6. apt update

if any issues try
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -


7. apt install timescaledb-2-postgresql-12

8.apt-get update

9. apt-get install postgresql-client

10. exit root

11. docker exec -it <container id> psql 

12. CREATE EXTENSION IF NOT EXISTS timescaledb;

13 add shared_preload_libraries = 'timescaledb' into the path /data/db/postgresql.conf and restart the thingsboard service
 docker restart postgres_container_id_or_name

14. docker exec -it postgres_container_id_or_name psql

15. CREATE EXTENSION IF NOT EXISTS timescaledb;

16. \dx to check extensions

17. To add UUID to each sensor reading in ThingsBoard, you can use the `uuid-ossp` extension provided by PostgreSQL. Here are the steps:

1. **Connect to your ThingsBoard PostgreSQL Database:**
   Open your PostgreSQL client (e.g., pgAdmin) and connect to your ThingsBoard database.

2. **Enable the `uuid-ossp` Extension:**
   Run the following SQL command to enable the `uuid-ossp` extension in your database:
   ```sql
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   ```

3. **Add a UUID Column to the Table Storing Sensor Readings (ts_kv):**
   Assuming that the sensor readings are stored in the `ts_kv` table, you can add a new column for UUID:
   ```sql
   ALTER TABLE ts_kv
   ADD COLUMN IF NOT EXISTS uuid UUID DEFAULT uuid_generate_v4();
   ```

   This command adds a new column named `uuid` to the `ts_kv` table with the default value generated by `uuid_generate_v4()`.

4. **Update Existing Rows with UUIDs (Optional):**
   If you want to populate the newly added `uuid` column for existing rows, you can run the following SQL command:
   ```sql
   UPDATE ts_kv
   SET uuid = uuid_generate_v4()
   WHERE uuid IS NULL;
   ```

   This command sets a UUID for rows where the `uuid` column is currently NULL.

5. **View the UUID Column in pgAdmin:**
   Open pgAdmin and navigate to your ThingsBoard database. In the "Objects" tab, go to "Tables" and find the `ts_kv` table. You should see the newly added `uuid` column.

6. **Query Data with UUIDs:**
   You can now query data with the UUIDs. For example, to retrieve data with UUIDs, you can use a query like this:


`

   Replace the column names with the actual column names used in your `ts_kv` table.

By following these steps, you'll add a UUID column to your sensor readings in ThingsBoard, and you should be able to view and query it in pgAdmin. Remember to adjust the column names if your actual table structure differs.


SELECT entity_id, ts, key, long_v, dbl_v, bool_v, str_v, uuid
FROM ts_kv
ORDER BY ts DESC  -- Assuming you want to order by the timestamp in descending order
LIMIT 50;


SELECT entity_id, ts, key, uuid
FROM ts_kv
ORDER BY ts DESC  -- Assuming you want to order by the timestamp in descending order
LIMIT 10;

SELECT DISTINCT entity_id
FROM ts_kv;


 <!-- understand OWL -->
 <!-- https://chrdebru.github.io/courses/ois/ -->

 <!-- RASA TEXTTO SPEECH -->
 <!-- https://github.com/Anwarvic/RasaChatbot-with-ASR-and-TTS -->
 <!-- https://github.com/srichakradhar/rasa-chatbot -->

<!-- rasa full -->
 <!-- https://vimeo.com/254777331 -->
