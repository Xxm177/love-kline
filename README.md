# Love Kline

关系 K 线分析系统 — 上传聊天记录，AI 分析情感，生成关系 K 线走势图。

## 功能

- 上传微信/QQ 聊天记录（txt）
- DeepSeek AI 批量评分每条消息（-5 ~ +5）
- 累积生成关系指数曲线
- 生成日 K 线 OHLC 数据
- K 线图可视化（ECharts 蜡烛图）
- Excel 导出（3 个 Sheet）

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.13 / FastAPI / Pydantic v2 |
| AI | DeepSeek Chat API |
| 前端 | Vue 3 / Vite / TypeScript / Element Plus / ECharts |
| Excel | openpyxl |
| 部署 | Docker / docker-compose |

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Xxm177/love-kline.git
cd love-kline
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入 DeepSeek API Key：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 3. 启动后端

```bash
uv sync
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:3000`。

### 5. Docker 一键启动

```bash
docker-compose up -d
```

## 聊天记录格式

```
2025-06-01 08:00 小明：早安宝贝
2025-06-01 09:00 小红：早安亲爱的
2025-06-01 10:00 小明：想你了
```

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/upload` | 上传并解析聊天记录 |
| POST | `/analyze` | 单条消息评分 |
| POST | `/generate-kline` | 一键分析（上传→评分→指数→K线） |
| POST | `/export` | 导出 Excel |
