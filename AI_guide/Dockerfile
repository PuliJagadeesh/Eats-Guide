# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set up cache and flagging directories with the correct permissions
ENV TRANSFORMERS_CACHE=/app/cache
ENV GRADIO_FLAGGING_DIR=/app/gradio_flagged
RUN mkdir -p /app/cache /app/gradio_flagged && chmod -R 777 /app/cache /app/gradio_flagged

# Copy the .env file for environment variables
COPY .env /app/.env

# Expose the port the app runs on
EXPOSE 7860

# Command to run the main.py script
CMD ["python", "main.py"]
