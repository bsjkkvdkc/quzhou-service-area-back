FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py migrate

RUN python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '1320843434@qq.com', 'admin') if not User.objects.filter(username='admin').exists() else print('exists')"

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2"]
