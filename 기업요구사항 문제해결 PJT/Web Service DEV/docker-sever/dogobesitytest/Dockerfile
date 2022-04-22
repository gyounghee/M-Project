FROM python:3.9.7

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim
RUN apt-get -y install libgl1-mesa-glx

RUN mkdir /srv/docker-server
ADD . /srv/docker-server

WORKDIR /srv/docker-server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#EXPOSE 9000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
