FROM python:3.9

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY job.py .

CMD ["python", "job.py"]
