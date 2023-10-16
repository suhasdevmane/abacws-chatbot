# Use a base image with OpenJDK 11
FROM openjdk:11

# Set the working directory
WORKDIR /app

# Download and install ThingsBoard DEB package
RUN apt update && apt install -y wget

# Install necessary packages
RUN apt update && apt install -y wget openjdk-11-jre-headless

RUN wget https://github.com/thingsboard/thingsboard/releases/download/v3.6/thingsboard-3.6.deb
RUN dpkg -i thingsboard-3.6.deb

# Edit ThingsBoard configuration
RUN echo "export DATABASE_TS_TYPE=timescale" >> /etc/thingsboard/conf/thingsboard.conf
RUN echo "export SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/thingsboard" >> /etc/thingsboard/conf/thingsboard.conf
RUN echo "export SPRING_DATASOURCE_USERNAME=postgres" >> /etc/thingsboard/conf/thingsboard.conf
RUN echo "export SPRING_DATASOURCE_PASSWORD=postgres" >> /etc/thingsboard/conf/thingsboard.conf
RUN echo "export SQL_TIMESCALE_CHUNK_TIME_INTERVAL=604800000" >> /etc/thingsboard/conf/thingsboard.conf

# Run the installation script and load demo data
RUN /usr/share/thingsboard/bin/install/install.sh --loadDemo

# Expose the ThingsBoard port
EXPOSE 8080

# Start ThingsBoard
RUN service thingsboard start
