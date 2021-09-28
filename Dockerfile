FROM python:3.8

WORKDIR /search-categories-api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./api ./api

CMD ["python", "./api/api.py"]
