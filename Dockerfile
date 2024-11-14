# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the AWS region as an environment variable
ENV AWS_DEFAULT_REGION=ap-south-1 

# Expose port 8080 for the Flask app
EXPOSE 8080

# Define environment variable for Flask
ENV FLASK_APP=run.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
