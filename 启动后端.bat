@echo off
chcp 65001 >nul
echo ========================================
echo  安徽科技工程大学高考专业推荐系统
echo ========================================
echo.

cd /d "%~dp0"

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

REM 创建虚拟环境
echo [1/5] 创建虚拟环境...
if not exist "backend\venv" (
    cd backend
    python -m venv venv
    cd ..
)

REM 激活虚拟环境并安装依赖
echo [2/5] 安装后端依赖...
cd backend
call venv\Scripts\activate.bat
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 python-dotenv==1.0.0
if errorlevel 1 (
    echo [警告] pip安装遇到问题，尝试直接使用系统Python...
    pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 python-dotenv==1.0.0
)

REM 数据库迁移
echo [3/5] 数据库迁移...
python manage.py makemigrations
python manage.py migrate

REM 导入数据
echo [4/5] 导入示例数据...
python ..\database\import_data.py

REM 启动后端
echo [5/5] 启动后端服务...
echo 后端已启动: http://localhost:8000
start "" "http://localhost:8000/api/"
python manage.py runserver 8000
