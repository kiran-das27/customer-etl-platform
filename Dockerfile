FROM apache/spark:3.5.1-python3

WORKDIR /app

COPY src/ .

CMD ["python", "customer_job.py"]