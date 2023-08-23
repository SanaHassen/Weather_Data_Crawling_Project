FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY crawler.py crawler.py
COPY city.list.json city.list.json
COPY init_db.py init_db.py


CMD ["python", "crawler.py"]
