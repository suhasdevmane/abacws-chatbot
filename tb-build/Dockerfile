# Use a base image with Ubuntu 20.04
FROM ubuntu:20.04

# Update the package list and install required packages
RUN apt update && apt install -y openjdk-11-jdk wget

# Download and install ThingsBoard
RUN wget https://github.com/thingsboard/thingsboard/releases/download/v3.6/thingsboard-3.6.deb
RUN dpkg -i thingsboard-3.6.deb

# Install PostgreSQL and TimescaleDB
RUN apt install -y postgresql-12
# You can add PostgreSQL and TimescaleDB configuration here

# Expose necessary ports
EXPOSE 8080

# Start ThingsBoard
CMD ["/usr/share/thingsboard/bin/install/install.sh", "--loadDemo"]

# You may want to add the commands to start the PostgreSQL and TimescaleDB services here
