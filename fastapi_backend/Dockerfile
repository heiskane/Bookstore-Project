FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV TESTING=i_hate_this_workaround

WORKDIR /app/

COPY app/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /app

ENV PYTHONPATH=/app