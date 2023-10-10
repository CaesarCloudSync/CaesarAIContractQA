# Use the official Python 3.9 image
#FROM python:3.9
FROM ubuntu:latest
RUN apt update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip python-dev-is-python3 libmysqlclient-dev 
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config 
RUN apt install graphviz libgraphviz-dev -y
RUN rm -rf /var/lib/apt/lists/*
#  
# 
RUN export PYTHONPATH=$PWD

RUN pip install uvicorn
# Set the working directory to /code
WORKDIR /code
#VOLUME /home/amari/Desktop/CaesarAI/CaesarFastAPI /code
# Copy the current directory contents into the container at /code
COPY ./requirements.txt /code/requirements.txt
 
# Install requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user
# Switch to the "user" user
USER user
# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

# Local
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860","--reload"] 
# Fly.io
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080","--reload"] 