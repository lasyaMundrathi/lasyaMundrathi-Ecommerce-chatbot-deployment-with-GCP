# Use official Python image from DockerHub
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the port Streamlit uses
EXPOSE 8080

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_PORT=8080

# Run the application
CMD ["streamlit", "run", "app.py"]

