# K8s Manager

一个轻量级的Kubernetes集群管理平台，提供Web界面来管理Pod、Deployment、Service等资源。

## 功能特性

- 🎯 **多集群支持** - 管理多个K8s集群
- 📊 **Pod管理** - 查看、删除、日志查看、实时监控
- 🚀 **Deployment管理** - 部署应用、更新、扩缩容、回滚
- 🔧 **Service管理** - 网络配置和服务暴露
- 📈 **基础监控** - 资源使用情况实时显示
- 🔐 **权限管理** - 基于RBAC的访问控制（计划中）

## 技术栈

### 后端
- Python 3.9+
- FastAPI
- kubernetes-client
- Pydantic

### 前端
- Vue 3
- TypeScript
- Element Plus
- Axios

## 快速开始

### Docker Compose启动（推荐）

```bash
git clone https://github.com/Zhq7777/k8s-manager.git
cd k8s-manager
cp backend/.env.example backend/.env
# 编辑backend/.env，配置KUBECONFIG_PATH
docker-compose up -d
```

访问：
- 前端: http://localhost
- API文档: http://localhost:8000/docs

### 本地开发启动

**后端**：
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

**前端**：
```bash
cd frontend
npm install
npm run dev
```

### Kubernetes部署

```bash
kubectl create namespace k8s-manager
kubectl apply -f k8s/
```

## 文档

- [安装指南](docs/installation.md)
- [使用指南](docs/usage.md)
- [API文档](docs/api.md)
- [部署指南](docs/deployment.md)
- [开发指南](docs/development.md)

## 许可证

MIT
