FROM python:3.9-slim

ENV TOKENIZERS_PARALLELISM=false

RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libasound-dev \
    default-jre-headless \
    wget \
    curl \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

RUN pip install --upgrade pip
RUN pip install --no-cache-dir numpy==1.23.5

COPY requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader averaged_perceptron_tagger averaged_perceptron_tagger_eng cmudict

COPY backend/ /app/backend/

CMD ["python", "app.py"]