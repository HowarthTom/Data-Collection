FROM python:3.10.2-slim-buster

RUN apt-get update
#install system depend
RUN apt-get install -y software-properties-common


# Install Firefox and GeckoDriver
RUN apt-get update && apt-get install -y firefox-esr && apt-get install -y wget && \
    wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" -O geckodriver.tgz && \
    tar -xvzf geckodriver.tgz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver.tgz

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

# Disables buffering to allow continuous output
ENV PYTHONBUFFERED 1

# Sets the entrypoint when the dockerfile runs
CMD ["python3", "scraper.py"]