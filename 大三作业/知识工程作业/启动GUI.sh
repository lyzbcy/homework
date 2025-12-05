#!/bin/bash

echo "========================================"
echo "  医疗知识图谱问答系统 - GUI启动"
echo "========================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python，请先安装Python 3.6+"
    exit 1
fi

echo "[1/3] 检查依赖包..."
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[提示] 正在安装PyQt5..."
    pip3 install PyQt5 matplotlib networkx
fi

echo "[2/3] 检查Neo4j连接..."
python3 -c "from py2neo import Graph; g = Graph('bolt://localhost:7687', auth=('neo4j', 'tangyudiadid0')); print('连接成功')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[警告] 无法连接到Neo4j数据库"
    echo "[提示] 请确保Neo4j服务已启动"
    read -p "[提示] 按回车键继续启动GUI（可能无法正常使用）..."
fi

echo "[3/3] 启动图形界面..."
echo ""
python3 gui_chatbot.py


