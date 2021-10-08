FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV TESTING=i_hate_this_workaround

COPY ./app /app/app
COPY ./prestart.sh /app
COPY ./create_tables.py /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt