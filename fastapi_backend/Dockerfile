FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app
COPY ./prestart.sh /app
COPY ./create_tables.py /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt