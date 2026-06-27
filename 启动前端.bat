@echo off
chcp 65001 >nul
echo ========================================
echo  前端开发服务器启动
echo ========================================
echo.

cd /d "%~dp0"

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Node.js，请先安装Node.js 16+
    pause
    exit /b 1
)

REM 安装依赖
echo [1/3] 安装前端依赖...
if not exist "node_modules" (
    npm install
    if errorlevel 1 (
        echo [警告] npm安装遇到问题，尝试使用淘宝镜像...
        npm config set registry https://registry.npmmirror.com
        npm install
    )
)

REM 启动前端
echo [2/3] 启动前端服务...
echo 前端已启动: http://localhost:3000
echo 请在浏览器中打开此地址
start "" "http://localhost:3000"

echo [3/3] 运行开发服务器...
npm run dev
