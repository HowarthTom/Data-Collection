FROM python:3.10.2-slim-buster


# Disables buffering to allow continuous output
ENV PYTHONBUFFERED 1

# RUN apt-get update
# RUN apt-get install -y wget
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install sudo
# RUN sudo apt-get update
# RUN sudo apt-get install -f
# RUN apt-get install ./google-chrome-stable_current_amd64.deb


# Creates the /app directory 
RUN mkdir /app

# Sets /app as the working directory
WORKDIR /app

# Copies required files to the directory
COPY initialiser.py /app/
COPY items.py /app/
COPY saver.py /app/
COPY scraper.py /app/
COPY requirements.txt /app/

# Installs the dependencies 
RUN pip install -r requirements.txt

# Sets the entrypoint when the dockerfile runs
CMD ["python3", "scraper.py"]