# Use an official Rasa SDK image as a parent image
FROM rasa/rasa-sdk:latest

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app/actions/
# Install any needed packages specified in requirements.txt as the root user
USER root

COPY . /app/actions
RUN pip install -r /app/actions/requirements.txt

# Change back to the non-root user provided by the Rasa SDK image
USER 1001

# Expose the default Rasa Action Server port
EXPOSE 5055

# Start the Rasa Action Server
CMD ["start", "--actions", "actions"]
