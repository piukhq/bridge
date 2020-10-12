FROM binkhq/python:3.9

WORKDIR /app
ADD . .

RUN apt-get update && apt-get -y install git && \
    pip --no-cache-dir install pipenv && \
    pipenv install --system --deploy --ignore-pipfile && \
    apt-get -y autoremove git && rm -rf /var/lib/apt/lists

CMD ["gunicorn", "--workers=2", "--threads=2", "--error-logfile=-", \
     "--access-logfile=-", "--bind=0.0.0.0:9000", "bridge.server"]
