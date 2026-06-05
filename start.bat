@echo off
title Love Kline - Backend & Frontend

echo ================================
echo   Love Kline
echo   后端: http://localhost:8000
echo   前端: http://localhost:3000
echo ================================
echo.

echo [1/2] 启动后端...
start "Love Kline - Backend" cmd /c "cd /d %~dp0 && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo [2/2] 启动前端...
start "Love Kline - Frontend" cmd /c "cd /d %~dp0frontend && npm run dev"

echo.
echo 启动完成，浏览器打开 http://localhost:3000
echo 关闭请直接关掉两个弹窗。
