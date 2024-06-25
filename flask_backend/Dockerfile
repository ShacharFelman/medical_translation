FROM python:3.11

WORKDIR /src
COPY requirements.txt /src

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

CMD ["python3", "app.py"]
