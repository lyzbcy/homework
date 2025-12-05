#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：检查所有模块是否能正常导入
"""
import sys
import os

def test_imports():
    """测试所有必要的模块导入"""
    print("=" * 50)
    print("开始测试模块导入...")
    print("=" * 50)
    
    # 测试第三方库
    try:
        import py2neo
        print("✓ py2neo 导入成功")
    except ImportError as e:
        print("✗ py2neo 导入失败:", e)
        print("  请运行: pip install py2neo")
        return False
    
    try:
        import ahocorasick
        print("✓ ahocorasick 导入成功")
    except ImportError as e:
        print("✗ ahocorasick 导入失败:", e)
        print("  请运行: pip install pyahocorasick")
        return False
    
    # 测试项目模块
    try:
        from question_classifier import QuestionClassifier
        print("✓ QuestionClassifier 导入成功")
    except Exception as e:
        print("✗ QuestionClassifier 导入失败:", e)
        return False
    
    try:
        from question_parser import QuestionPaser
        print("✓ QuestionPaser 导入成功")
    except Exception as e:
        print("✗ QuestionPaser 导入失败:", e)
        return False
    
    try:
        from answer_search import AnswerSearcher
        print("✓ AnswerSearcher 导入成功")
    except Exception as e:
        print("✗ AnswerSearcher 导入失败:", e)
        return False
    
    try:
        from chatbot_graph import ChatBotGraph
        print("✓ ChatBotGraph 导入成功")
    except Exception as e:
        print("✗ ChatBotGraph 导入失败:", e)
        return False
    
    print("=" * 50)
    print("所有模块导入测试完成！")
    print("=" * 50)
    
    # 测试初始化（不连接数据库）
    print("\n测试类初始化（不连接数据库）...")
    try:
        classifier = QuestionClassifier()
        print("✓ QuestionClassifier 初始化成功")
    except Exception as e:
        print("✗ QuestionClassifier 初始化失败:", e)
        return False
    
    print("\n所有测试通过！")
    print("\n注意：")
    print("1. 确保已安装所有依赖: pip install -r requirements.txt")
    print("2. 确保 Neo4j 数据库正在运行")
    print("3. 确保 Neo4j 连接配置正确（localhost:7474, 用户名: neo4j, 密码: tangyudiadid0）")
    print("4. 如果还未构建知识图谱，请先运行 build_medicalgraph.py")
    
    return True

if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)

