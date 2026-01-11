#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证文档分析器功能
"""

from document_analyzer import DocumentAnalyzer

def test_load_documents():
    """测试文档加载"""
    print("=" * 60)
    print("测试1: 文档加载")
    print("=" * 60)
    
    analyzer = DocumentAnalyzer()
    analyzer.load_documents()
    
    info = analyzer.get_document_info()
    print("\n文档信息：")
    for path, details in info.items():
        print(f"  文件: {details['文件名']}")
        print(f"  页数: {details['总页数']}")
        print(f"  状态: {details['状态']}")
        print()
    
    return analyzer

def test_search(analyzer):
    """测试搜索功能"""
    print("=" * 60)
    print("测试2: 搜索功能")
    print("=" * 60)
    
    keywords = ["机器人", "电池", "尺寸"]
    
    for keyword in keywords:
        results = analyzer.search_in_documents(keyword)
        print(f"\n关键词 '{keyword}': 找到 {len(results)} 处匹配")
        
        if results:
            print(f"  示例: {results[0]['document']}, 第{results[0]['page']}页")

def test_analyze(analyzer):
    """测试问答功能"""
    print("\n" + "=" * 60)
    print("测试3: 问答功能")
    print("=" * 60)
    
    questions = [
        "机器人的尺寸要求",
        "电池安全规范"
    ]
    
    for question in questions:
        print(f"\n问题: {question}")
        answer = analyzer.analyze(question)
        print(answer)

if __name__ == "__main__":
    print("文件内容分析专家系统 - 功能测试\n")
    
    # 测试1: 加载文档
    analyzer = test_load_documents()
    
    # 测试2: 搜索功能
    test_search(analyzer)
    
    # 测试3: 问答功能
    test_analyze(analyzer)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
