# Use the official Python image from Docker Hub
FROM python:3.12.1-slim

# Set environment variables to ensure Python runs in an optimal way
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a directory for the app
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that the Flask app runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD ["flask", "run"]
