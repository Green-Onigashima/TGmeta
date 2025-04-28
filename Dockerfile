# Use official Python image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed dependencies (if you have requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]
