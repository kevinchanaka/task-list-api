FROM python:3.9

ENV NUM_WORKERS=4

COPY . /app

WORKDIR /app

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

EXPOSE 8000

ENTRYPOINT ["/bin/bash", "-c", "gunicorn -w $NUM_WORKERS -b 0.0.0.0:8000 app:app;"]
