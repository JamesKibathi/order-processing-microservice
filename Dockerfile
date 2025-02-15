FROM python:3.8.0

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.wsgi:application"]
