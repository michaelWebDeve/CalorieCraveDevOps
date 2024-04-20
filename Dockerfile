# Python image
FROM python:3.9.11-slim-buster

# Working directory within the container
WORKDIR /app

# Copy the requirements into the container
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable FLASK_APP to your application file
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port
EXPOSE 5000

# Start the application
CMD ["flask", "run"]