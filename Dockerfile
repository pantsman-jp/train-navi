FROM python:3.13.4

WORKDIR /app

COPY . /app

RUN pip install flask jpholiday requests beautifulsoup4

CMD ["python", "app.py"]
