#!/bin/bash
app="traffic-fc"
docker build -t ${app} .
docker run -d -p 5006:5006 \
  --name=${app} \
  -v $PWD:/app ${app}
