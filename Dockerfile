FROM ubuntu:xenial-20191212

WORKDIR /app

COPY ./app .

RUN apt-get update \
  && apt-get -y install python3 \
  && apt-get -y install python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install flask

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV FLASK_APP=app

CMD ["flask", "run", "--host=0.0.0.0"]
