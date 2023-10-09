This project is under development.


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


```
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
After executing this command you can open http://{yor-host-ip}:9090 in your browser. You should see ThingsBoard login page. Use the following default credentials:

Systen Administrator: sysadmin@thingsboard.org / sysadmin
Tenant Administrator: tenant@thingsboard.org / tenant
Customer User: customer@thingsboard.org / customer
You can always change passwords for each account in account profile page.

You can detach from session terminal with Ctrl-p Ctrl-q - the container will keep running in the background.

To reattach to the terminal (to see ThingsBoard logs) run:

$ docker attach mytb

To stop the container:

$ docker stop mytb

To start the container:

$ docker start mytb






Owner: Suhas Devmane
Contact: suhasdevmane@outlook.com