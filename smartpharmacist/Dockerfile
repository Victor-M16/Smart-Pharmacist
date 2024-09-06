# Use an official Python image as the base
FROM python:3.11-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project files to the container
COPY . /app/

# Build Tailwind CSS before starting the app
RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the app
EXPOSE 8000

# Command to run the app with Gunicorn
CMD gunicorn --timeout 90 smartpharmacist.wsgi
