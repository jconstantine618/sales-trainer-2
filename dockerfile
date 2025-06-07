FROM python:3.11-slim
WORKDIR /app
COPY ./sales_trainer /app
RUN pip install -U pip && pip install -r /app/requirements.txt
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker",
     "api.main:app", "--bind", "0.0.0.0:8000"]

