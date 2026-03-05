# SoulGuard 部署指南

## 系统要求

- Python 3.8+
- Linux/macOS/Windows
- 内存: 512MB+
- 磁盘: 100MB+

## 安装步骤

### 1. 安装依赖

```bash
pip install mem0ai numpy scikit-learn psutil
```

### 2. 配置环境变量

```bash
export KIMI_API_KEY=your-api-key
export OPENAI_BASE_URL=https://api.siliconflow.cn/v1
```

### 3. 启动系统

```bash
# 启动守护进程
./start_daemon.sh

# 启动监控面板
./start_dashboard.sh
```

## Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 18790

CMD ["./start_dashboard.sh"]
```

## 生产环境建议

1. 使用systemd管理服务
2. 配置日志轮转
3. 定期备份数据
4. 监控资源使用
