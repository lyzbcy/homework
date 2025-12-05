@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   医疗知识图谱问答系统 - GUI启动
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

echo [1/3] 检查依赖包...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [错误] PyQt5未安装
    echo [提示] 请先运行"安装依赖.bat"安装所有依赖包
    echo [提示] 或手动运行: pip install PyQt5 matplotlib networkx
    pause
    exit /b 1
)

python -c "import networkx" >nul 2>&1
if errorlevel 1 (
    echo [错误] networkx未安装
    echo [提示] 请先运行"安装依赖.bat"安装所有依赖包
    echo [提示] 或手动运行: pip install networkx
    pause
    exit /b 1
)

python -c "import matplotlib" >nul 2>&1
if errorlevel 1 (
    echo [错误] matplotlib未安装
    echo [提示] 请先运行"安装依赖.bat"安装所有依赖包
    echo [提示] 或手动运行: pip install matplotlib
    pause
    exit /b 1
)

echo [2/3] 检查Neo4j连接...
python -c "from py2neo import Graph; g = Graph('bolt://localhost:7687', auth=('neo4j', 'tangyudiadid0')); g.run('RETURN 1'); print('连接成功')" >nul 2>&1
if errorlevel 1 (
    echo [警告] 无法连接到Neo4j数据库
    echo [提示] 请确保Neo4j服务已启动
    echo [提示] 按任意键继续启动GUI...
    pause >nul
)

echo [3/3] 启动图形界面...
echo.
echo [提示] 系统已支持以下新功能：
echo   - 药物禁忌查询
echo   - 不良反应查询
echo   - 注意事项查询
echo   - 特殊人群用药
echo   - 药物成份查询
echo   - 症状导致疾病
echo   - 科室查询
echo   - 部位查询
echo.
echo [提示] 如需使用新功能，请确保已运行 import_enhanced_data.py 导入增强数据
echo.
python gui_chatbot.py

if errorlevel 1 (
    echo.
    echo [错误] 启动失败，请检查错误信息
    pause
)

