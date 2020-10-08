FROM binkhq/python:3.8

WORKDIR /app
ADD . .

RUN apt update && apt -y install git && \
    pip --no-cache-dir install pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    apt-get -y autoremove git && rm -rf /var/lib/apt/lists

CMD ["gunicorn", "--workers=2", "--threads=2", "--error-logfile=-", \
     "--access-logfile=-", "--bind=0.0.0.0:9000", "bridge.server"]
