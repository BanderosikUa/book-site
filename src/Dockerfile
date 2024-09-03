FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /usr/src/book-site

RUN apt-get update -y && \
    apt-get upgrade -y

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/book-site

EXPOSE 8000
#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=config.settings.local" ]
