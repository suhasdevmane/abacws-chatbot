# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .
COPY app.py .
COPY Dockerfile .

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SentencePiece
RUN apt-get update && apt-get install -y \
    libprotobuf-dev \
    protobuf-compiler \
    && pip install sentencepiece \
    && pip install SPARQLWrapper \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY app.py .
COPY ./T5-SPARQL2QA/trained  /app/T5-SPARQL2QA/trained 
COPY ./T5-NL2SPARQL/trained  /app/T5-NL2SPARQL/trained
# COPY ./BART-NL2SPARQL/trained  /app/BART-NL2SPARQL/trained     Replace this BART Model with t5 model for below t5-nl2sparql

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

