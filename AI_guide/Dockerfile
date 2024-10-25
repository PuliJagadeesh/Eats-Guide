# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your .env file (ensure sensitive keys are stored securely)
COPY .env /app/.env

# Expose the port the app runs on
EXPOSE 7860

# Command to run the main.py script
CMD ["python", "main.py"]

