# Dockerfile
# Use the official Python image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /bud

# Copy the source code into the container
COPY . /bud

# Install required Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the job manager when the container starts
CMD ["python", "main.py"]
