# python app dockerfile

FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["python", "app.py"]
