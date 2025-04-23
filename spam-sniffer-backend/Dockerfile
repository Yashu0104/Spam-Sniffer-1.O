<<<<<<< HEAD
# Use official Python image
FROM python:3.10-slim

# Set work directory
=======
# Use official Python base image
FROM python:3.10-slim

# Set working directory
>>>>>>> 5dd13c4 (Made Docker Containers for front-end and Back-end)
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

<<<<<<< HEAD
# Download punkt and punkt_tab manually at build time
RUN python -m nltk.downloader punkt punkt_tab

# Copy app code
COPY . .

# Expose the port
EXPOSE 5000

# Run the application
=======
# Copy all backend files (model files, app.py, etc.)
COPY . .

# Expose the Flask default port
EXPOSE 5000

# Run the Flask app
>>>>>>> 5dd13c4 (Made Docker Containers for front-end and Back-end)
CMD ["python", "app.py"]
