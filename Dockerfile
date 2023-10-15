FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update \
    && apt-get install -y libpq-dev gcc

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "image_predictor_api:app", "--host", "0.0.0.0", "--port", "8000"]
