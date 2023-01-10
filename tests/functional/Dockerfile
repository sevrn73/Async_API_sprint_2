FROM python:3.9

WORKDIR /tests/functional

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["/tests/functional/docker-entrypoint.sh"]