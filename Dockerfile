# Base image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a directory for the app
RUN mkdir /app
WORKDIR /app

# Install SSH server
RUN apt-get update && apt-get install -y openssh-server && apt-get clean

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose the necessary ports
EXPOSE 8080 22

# Add the initialization script
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Start the SSH service and the Flask app
CMD ["/app/start.sh"]
