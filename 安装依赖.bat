@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   安装医疗知识图谱问答系统依赖
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

echo [信息] 当前Python版本:
python --version
echo.

echo [信息] 当前pip版本:
python -m pip --version
echo.

echo [1/4] 安装基础依赖包...
python -m pip install --upgrade pip
python -m pip install py2neo>=2021.2.3
python -m pip install pyahocorasick>=2.0.0
python -m pip install pymongo>=4.0.0
python -m pip install lxml>=4.6.0
echo.

echo [2/4] 安装GUI依赖包...
python -m pip install PyQt5>=5.15.0
python -m pip install matplotlib>=3.5.0
python -m pip install networkx>=2.6.0
echo.

echo [3/4] 验证安装...
python -c "import PyQt5; print('PyQt5: OK')" 2>nul || echo PyQt5: 失败
python -c "import matplotlib; print('matplotlib: OK')" 2>nul || echo matplotlib: 失败
python -c "import networkx; print('networkx: OK')" 2>nul || echo networkx: 失败
python -c "import py2neo; print('py2neo: OK')" 2>nul || echo py2neo: 失败
echo.

echo [4/4] 安装完成！
echo.
echo 如果看到"失败"信息，请手动运行:
echo   pip install [包名]
echo.
pause


