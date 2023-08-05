FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

ENV FLASK_APP=app/run.py

ENV FLASK_RUN_HOST=0.0.0.0

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the Flask application
CMD ["flask", "run"]


