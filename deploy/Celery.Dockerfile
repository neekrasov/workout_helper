FROM python:3.11.0
WORKDIR /usr/src/workout_helper

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./


RUN pip install --upgrade pip

RUN pip install poetry
RUN poetry install --without dev --no-root
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

RUN wget https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chown root:root /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

COPY . ./

CMD make run-celery