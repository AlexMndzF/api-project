FROM python:3.7-slim

# Copy the contents of the current directory inside the docker image
ADD . /app

# Set the home of the docker image
WORKDIR /app

# Install the requirements 
RUN pip3 install -r requirements.txt 

# Command to run when starting the container
CMD ["python3","-u","app.py"]