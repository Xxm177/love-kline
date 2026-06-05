# Love Kline

关系 K 线分析系统 — 上传聊天记录，AI 分析情感，生成关系 K 线走势图。

## 功能

- 上传微信/QQ 聊天记录（txt）
- DeepSeek AI 批量评分每条消息（-5 ~ +5）
- 累积生成关系指数曲线
- 生成日 K 线 OHLC 数据
- K 线图可视化（ECharts 蜡烛图 + MA5/MA10 均线 + 消息量柱状图）
- 情感维度分布饼图、消息评分详情列表
- 一键导出 K 线 PNG 图片
- 异步任务 + 实时进度条，支持 10 万+ 条消息
- 后端支持 Excel 导出，5 路并发批量评分
- 自动识别微信导出格式

## 项目结构

```
love-kline/
├── app/
│   ├── main.py                      # FastAPI 入口 + CORS
│   ├── api/
│   │   ├── upload.py                # POST /upload  上传解析
│   │   ├── analyze.py               # POST /analyze  单条评分
│   │   ├── kline.py                 # POST /kline + /generate-kline  生成K线
│   │   └── export.py                # POST /export  Excel导出
│   ├── services/
│   │   ├── parser.py                # 聊天记录解析
│   │   ├── deepseek.py              # DeepSeek 单条/批量评分
│   │   ├── relation.py              # 关系指数累积
│   │   ├── kline_generator.py       # K线 OHLC 生成
│   │   └── exporter.py              # openpyxl Excel 导出
│   └── schemas/
│       └── analyze.py               # Pydantic v2 数据模型
├── frontend/
│   ├── src/
│   │   ├── App.vue                  # 主页面
│   │   ├── main.ts                  # Vue 入口
│   │   ├── api/index.ts             # API 调用层
│   │   ├── components/
│   │   │   ├── UploadArea.vue       # 上传区域
│   │   │   ├── AnalysisCards.vue    # 统计卡片 + 维度饼图
│   │   │   └── KlineChart.vue       # K线图 + 均线 + 消息量
│   │   └── styles/main.css          # 暗色主题
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── start.bat                        # Windows 一键启动
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

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

支持三种格式自动识别：

**格式 1 — 单行（推荐）**
```
2025-06-01 08:00 小明：早安宝贝
2025-06-01 09:00 小红：早安亲爱的
```

**格式 2 — 微信导出 A（发送者在前）**
```
小明  2025-06-01 08:00
早安宝贝

小红  2025-06-01 09:00
早安亲爱的
```

**格式 3 — 微信导出 B（时间在前）**
```
2025-06-01 08:00 小明
早安宝贝

2025-06-01 09:00 小红
早安亲爱的
```

## 性能说明

每 200 条消息为一批，5 路并发请求 DeepSeek，实测数据：

| 消息量 | 耗时 |
|--------|------|
| 100 条 | ~5 秒 |
| 1,000 条 | ~30 秒 |
| 5,000 条 | ~2 分钟 |
| 20,000 条 | ~8 分钟 |
| 50,000 条 | ~20 分钟 |

大文件自动使用异步模式：提交后后台跑，进度条实时显示，跑完出结果。支持 10 万+ 条消息，卡住的批次自动跳过不丢数据。

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/upload` | 上传并解析聊天记录 |
| POST | `/analyze` | 单条消息评分 |
| POST | `/generate-kline` | 同步分析（小文件，< 1000 条） |
| POST | `/generate-kline-async` | 异步分析（大文件，带进度条） |
| GET | `/task/{task_id}` | 查询异步任务进度与结果 |
| POST | `/export` | 导出 Excel（3 个 Sheet） |
