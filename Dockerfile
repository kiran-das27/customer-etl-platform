FROM python:3.11-slim

# Install Java
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean
    
# Set Java path
ENV JAVA_HOME=/usr/lib/jvm/default-java


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY src/ .


CMD ["python","customer_job.py"]
