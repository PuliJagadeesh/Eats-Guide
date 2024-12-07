# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy requirements.txt to the working directory in the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


# Set a custom cache directory for Hugging Face Transformers
ENV HF_HOME=/app/cache/huggingface

# Copy the .env file for environment variables
COPY .env /app/.env

# Expose the port the app runs on
EXPOSE 7860

# Command to run the main.py script
CMD ["python", "main.py"]
