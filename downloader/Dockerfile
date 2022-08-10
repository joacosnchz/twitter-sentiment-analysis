FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY download_data.py .

RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get -y install vim

ENTRYPOINT ["python3", "download_data.py"]
