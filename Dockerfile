# FYI This deployement will take about 40 minutes without any logs.
# Due to sentence-transformers - |torch| nvidiacu11 other nvidia etc.
# Use the official Python 3.9 image
#FROM python:3.9
FROM ubuntu:latest
RUN apt update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip python-dev-is-python3 libmysqlclient-dev 
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config 
RUN apt install graphviz libgraphviz-dev -y
RUN rm -rf /var/lib/apt/lists/*

# TODO  Install Conda
# Install base utilities
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Insta
RUN export PYTHONPATH=$PWD

# Set the working directory to /code
WORKDIR /code
#VOLUME /home/amari/Desktop/CaesarAI/CaesarFastAPI /code
# Copy the current directory contents into the container at /code
COPY ./environment.yml /code/environment.yml
 
# Install requirements.txt 
RUN conda env create -f /code/environment.yml
RUN conda init bash
#RUN conda activate caesaraicontractqa

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
EXPOSE 8080
CMD /opt/conda/envs/caesaraicontractqa/bin/python ~/app/main.py
# Local
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860","--reload"] 
# Fly.io
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080","--reload"] 