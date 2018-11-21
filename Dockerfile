FROM python:3.6-alpine
MAINTAINER Omidiora Samuel <samparsky@gmail.com>
ENV PROJECT_DIR=bitcoin-etl

RUN mkdir /$PROJECT_DIR
WORKDIR /$PROJECT_DIR
COPY . .
RUN apk add --no-cache gcc musl-dev  #for C libraries: <limits.h> <stdio.h>
RUN pip install --upgrade pip && pip install -e /$PROJECT_DIR/

ENTRYPOINT ["python", "bitcoinetl"]