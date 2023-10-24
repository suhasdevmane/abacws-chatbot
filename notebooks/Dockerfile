# Use the jupyter/datascience-notebook as the base image
FROM jupyter/minimal-notebook:python-3.10
# Set the PATH to include the script directory
ENV PATH="/home/jovyan/.local/bin:${PATH}"
USER root
RUN apt-get update && \
    apt-get install -y libpq-dev && \
    apt-get clean && rm -rf var/lib/apt/lists/*
RUN apt-get update && \
    pip install --upgrade pip setuptools wheel
RUN apt-get update\
    && pip install --upgrade setuptools
RUN apt-get update \
    && apt-get -y install libpq-dev gcc 
RUN apt-get update -y && apt-get install -y portaudio19-dev
RUN pip install pyaudio
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --upgrade pocketsphinx
RUN pip install PyYAML==5.3.1
RUN pip install brickschema[all]
USER jovyan
# Copy the requirements.txt file into the container
# COPY requirements.txt /home/jovyan/requirements.txt

# Install Python packages from requirements.txt
# RUN pip install --no-cache-dir -r /home/jovyan/requirements.txt
