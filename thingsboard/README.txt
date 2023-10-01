
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
tenant- suhasdevmanemech@gmail.com
pass - Suhas@551993

docker compose up -d            #to up docker compose
docker compose down             # to stop docker-compose 
docker compose logs -f mytb    #to see logs
docker compose stop mytb
docker compose start mytb




pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=pgadmin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin

The default PostgreSQL user is thingsboard, default password is postgres. Please, put your credentials here instead of default.


Device-01
device token- 8lufFlQrrhMpJ4F5GHwm
curl -v -X POST http://localhost:8080/api/v1/8lufFlQrrhMpJ4F5GHwm/telemetry --header Content-Type:application/json --data "{temperature:25}"
mosquitto_pub -d -q 1 -h localhost -p 1883 -t v1/devices/me/telemetry -u 8lufFlQrrhMpJ4F5GHwm -m "{temperature:25}"

Device-02
curl -v -X POST http://localhost:8080/api/v1/MyJExSz1fCxSyQLmaHxD/telemetry --header Content-Type:application/json --data "{temperature:25}"
mosquitto_pub -d -q 1 -h localhost -p 1883 -t v1/devices/me/telemetry -u MyJExSz1fCxSyQLmaHxD -m "{temperature:25}"