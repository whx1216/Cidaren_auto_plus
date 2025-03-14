@echo off
chcp 65001

REM 检查虚拟环境文件夹是否存在
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo 虚拟环境不存在，正在创建...
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo 创建虚拟环境失败，请检查 Python 是否已安装并加入系统环境变量
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 检查依赖是否已安装（以 requirements.txt 中某个常见包为例，比如 pip install 依赖）
REM 此处假设 requirements.txt 存在
if exist requirements.txt (
    echo 安装或更新依赖...
    pip install -r requirements.txt
    IF ERRORLEVEL 1 (
        echo 安装依赖失败，请检查网络连接或 requirements.txt 配置
        pause
        call venv\Scripts\deactivate.bat
        exit /b 1
    )
) else (
    echo 未找到 requirements.txt，跳过依赖安装
)

REM 运行主程序
python main.py

REM 退出虚拟环境
call venv\Scripts\deactivate.bat

pause
