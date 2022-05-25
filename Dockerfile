FROM python:3.8

ENV APP_NAME=traffic.py
COPY /code/"$APP_NAME" /code/"$APP_NAME"
COPY /code/traffic.conf /code/traffic.conf
COPY /code/utils_traffic.py /code/utils_traffic.py
COPY /code/hereAPI /code/hereAPI

WORKDIR /code


ENV FLASK_APP="$APP_NAME"
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip3 install --no-cache-dir pip==22.1.1

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5006

CMD ["flask", "run"]
