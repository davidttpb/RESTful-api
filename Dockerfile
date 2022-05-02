# pull official base image
FROM python:3.10.3-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV APP_SETTINGS src.config.ProductionConfig


# new
# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# add and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# new
# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh


# add and run as non-root user
RUN adduser --disabled-password myuser
USER myuser


# run gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT manage:app