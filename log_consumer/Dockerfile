# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy consumer script and requirements
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the log consumer
CMD ["python", "log_consumer.py"]

