FROM ghcr.io/binkhq/python:3.10

WORKDIR /app
ADD . .

RUN apt-get update && apt-get -y install git && \
    pipenv install --system --deploy --ignore-pipfile && \
    apt-get -y autoremove git && rm -rf /var/lib/apt/lists

CMD ["gunicorn", "--workers=2", "--error-logfile=-", "--access-logfile=-", \
     "--bind=0.0.0.0:6502", "bridge.server"]
