FROM python:3.12-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 
    PYTHONUNBUFFERED=1 
    PIP_NO_CACHE_DIR=1

# 安装系统依赖
RUN apt-get update && apt-get install -y 
    gcc 
    libpq-dev 
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装Python依赖
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 复制项目文件
COPY . .

# 先执行数据库迁移，再创建管理员，最后收集静态文件
RUN python manage.py migrate
RUN python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '1320843434@qq.com', 'admin')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "2"]
