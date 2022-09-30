FROM python:3.10.7-slim-bullseye

WORKDIR /app/

COPY . /app/

RUN mkdir /app/.cache

RUN pip install -r ./requirements.txt

RUN playwright install

RUN playwright install-deps

WORKDIR /root/

RUN cp -R .cache/ms-playwright /app/.cache/ms-playwright

WORKDIR /app/

CMD uvicorn app:webserver --host 0.0.0.0 --port $PORT