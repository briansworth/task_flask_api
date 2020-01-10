FROM alpine:3.10

WORKDIR /app

COPY ./app .

RUN apk add --no-cache python3 libressl-dev py3-openssl \
  && pip3 install flask flask_restful pyopenssl

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV FLASK_APP=app

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
#CMD ["--cert=adhoc"]
