FROM python:3
RUN apt-get update && apt-get install -y iproute2 iputils-ping
WORKDIR /app
