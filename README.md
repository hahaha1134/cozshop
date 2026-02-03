# CozShop - 电商网站

一个基于 FastAPI + MongoDB + Vue 3 的现代化电商网站。

## 技术栈

### 后端
- FastAPI - 现代、快速的 Python Web 框架
- MongoDB - NoSQL 数据库
- JWT - 用户认证
- Pydantic - 数据验证

### 前端
- Vue 3 - 渐进式 JavaScript 框架
- Vite - 下一代前端构建工具
- Vue Router - 路由管理
- Pinia - 状态管理
- Axios - HTTP 客户端

## 功能特性

- ✅ 用户注册和登录
- ✅ JWT 身份验证
- ✅ 商品浏览和搜索
- ✅ 商品详情查看
- ✅ 购物车管理
- ✅ 订单创建和查看
- ✅ 响应式设计

## 项目结构

```
cozshop/
├── backend/           # 后端代码
│   ├── routers/      # API 路由
│   ├── models.py     # 数据模型
│   ├── auth.py       # 认证逻辑
│   ├── database.py   # 数据库连接
│   ├── config.py     # 配置文件
│   └── main.py       # 应用入口
└── frontend/         # 前端代码
    ├── src/
    │   ├── components/  # Vue 组件
    │   ├── views/       # 页面视图
    │   ├── stores/      # Pinia 状态管理
    │   ├── router/      # 路由配置
    │   └── utils/       # 工具函数
    └── vite.config.js   # Vite 配置
```

## 快速开始

### 前置要求

- Python 3.8+
- Node.js 16+
- MongoDB

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境（可选）：
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 `.env` 文件：
```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=cozshop
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. 初始化数据库：
```bash
python init_data.py
```

6. 启动后端服务：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

后端 API 将在 http://localhost:5000 运行

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

前端应用将在 http://localhost:5173 运行

## API 文档

启动后端服务后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## 默认账户

初始化数据后会创建以下管理员账户：
- 邮箱: admin@cozshop.com
- 密码: admin123

## 开发说明

### 后端开发

- API 路由位于 `backend/routers/` 目录
- 数据模型定义在 `backend/models.py`
- 数据库操作使用 Motor (异步 MongoDB 驱动)

### 前端开发

- 组件位于 `frontend/src/components/` 目录
- 页面视图位于 `frontend/src/views/` 目录
- 状态管理使用 Pinia，配置在 `frontend/src/stores/` 目录
- API 请求封装在 `frontend/src/utils/api.js`

## 部署

### 后端部署

1. 使用 Gunicorn + Uvicorn Workers：
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
```

2. 或使用 Docker（需要创建 Dockerfile）

### 前端部署

1. 构建生产版本：
```bash
npm run build
```

2. 将 `dist/` 目录部署到静态文件服务器（如 Nginx）

## 许可证

MIT License