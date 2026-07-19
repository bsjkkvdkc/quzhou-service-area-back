# 衢州服务区后端 API

浙江省商业集团有限公司衢州服务区官方网站后端服务

## 技术栈
- Django 6.0
- Django REST Framework
- PostgreSQL (腾讯云CDB)

## 本地开发
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 部署到腾讯云SCF

### 方式一：使用 Serverless 框架（推荐）
```bash
# 1. 安装 Serverless 框架
npm install -g serverless

# 2. 安装腾讯云插件
npm install serverless-tencent-cloud

# 3. 配置腾讯云密钥
sls config add

# 4. 部署
sls deploy
```

### 方式二：使用腾讯云控制台
1. 登录 [腾讯云控制台](https://console.cloud.tencent.com/scf)
2. 创建函数服务
3. 上传代码包
4. 配置环境变量和API网关

## API 接口
- `GET  /api/blogs/         - 博客列表
- `GET  /api/blogs/<id>/    - 博客详情
- `POST /api/feedbacks/     - 提交反馈
- `GET  /api/feedbacks/     - 反馈列表
- `GET  /api/feedback-stats/ - 反馈统计
