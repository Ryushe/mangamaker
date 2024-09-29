FROM python:3.12.5-slim

WORKDIR .

COPY requirements.txt . 

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run your application
CMD ["python", "./main.py"]