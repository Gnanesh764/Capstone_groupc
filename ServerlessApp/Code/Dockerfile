# this is an official Python runtime, used as the parent image
FROM python:3.7.0-slim

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# execute everyone's favorite pip command, pip install -r
RUN pip3 install -r requirements.txt

# unblock port 18004 for the flask app to run on
EXPOSE 18004

# execute the Flask app
CMD ["python3", "main.py"]