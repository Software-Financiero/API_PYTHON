FROM python:3.10.13

WORKDIR /API_PYTHON

COPY . /API_PYTHON/

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--reload"]