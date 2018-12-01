FROM python:3.7-alpine

RUN mkdir /app
COPY requirements.txt /app
COPY donatello/*.py /app/
WORKDIR /app

RUN apk add --no-cache --virtual build-dependencies gcc g++ musl-dev \
  && pip install -r requirements.txt \
  && apk del build-dependencies \
  && rm -r /root/.cache

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "-k", "gevent", "main:app"]
