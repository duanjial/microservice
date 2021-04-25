FROM python:3.9
ENV PYTHONUMBUFFERED 1
WORKDIR /app
ENV GOOGLE_APPLICATION_CREDENTIALS /app/key.json
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt \
    && apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y ffmpeg
COPY . /app