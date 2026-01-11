#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件内容分析专家系统
File Content Analysis Expert System

严格依据文件内容进行分析，绝不推测或引入外部知识。
"""

import os
import re
import json
from typing import List, Dict, Tuple, Optional


class DocumentAnalyzer:
    """
    文件内容分析专家
    
    核心原则：
    1. 严格依据原则 - 仅基于文件内容
    2. 零推测原则 - 不进行推断
    3. 完整性原则 - 全面覆盖相关内容
    4. 客观中立原则 - 保持客观
    """
    
    def __init__(self, config_path: str = "config.json"):
        """初始化分析器"""
        self.documents = {}
        self.document_paths = [
            "RoboMaster 2026 机甲大师高校系列赛机器人制作规范手册V1.0.0（20251021）.pdf",
            "RoboMaster 2026 机甲大师高校联盟赛比赛规则手册 V1.1.0（20251208）.pdf",
            "RoboMaster电池安全规范.pdf"
        ]
        self.text_cache = {}
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {config_path}: {e}")
        
        # 返回默认配置
        return {
            "search_settings": {
                "default_context_chars": 100,
                "max_results_display": 5
            },
            "answer_format": {
                "max_evidence_per_keyword": 3,
                "max_paragraph_chars": 200
            }
        }
        
    def load_documents(self):
        """
        加载三份文件
        
        注意：实际PDF读取需要PyMuPDF或PyPDF2库
        此处提供框架，实际实现时会读取PDF内容
        """
        try:
            import fitz  # PyMuPDF
            self._load_with_pymupdf()
        except ImportError:
            try:
                import PyPDF2
                self._load_with_pypdf2()
            except ImportError:
                print("警告: 未安装PDF处理库。请安装 PyMuPDF 或 PyPDF2")
                print("pip install PyMuPDF")
                self._load_placeholder()
    
    def _load_with_pymupdf(self):
        """使用PyMuPDF加载PDF文件"""
        import fitz
        
        for doc_path in self.document_paths:
            if os.path.exists(doc_path):
                try:
                    pdf_document = fitz.open(doc_path)
                    text_content = []
                    
                    for page_num in range(len(pdf_document)):
                        page = pdf_document[page_num]
                        text = page.get_text()
                        text_content.append({
                            'page': page_num + 1,
                            'text': text
                        })
                    
                    self.documents[doc_path] = {
                        'path': doc_path,
                        'pages': text_content,
                        'total_pages': len(pdf_document)
                    }
                    
                    pdf_document.close()
                    print(f"✓ 已加载: {doc_path}")
                    
                except Exception as e:
                    print(f"✗ 加载失败 {doc_path}: {e}")
            else:
                print(f"✗ 文件不存在: {doc_path}")
    
    def _load_with_pypdf2(self):
        """使用PyPDF2加载PDF文件"""
        import PyPDF2
        
        for doc_path in self.document_paths:
            if os.path.exists(doc_path):
                try:
                    with open(doc_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        text_content = []
                        
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            text = page.extract_text()
                            text_content.append({
                                'page': page_num + 1,
                                'text': text
                            })
                        
                        self.documents[doc_path] = {
                            'path': doc_path,
                            'pages': text_content,
                            'total_pages': len(pdf_reader.pages)
                        }
                    
                    print(f"✓ 已加载: {doc_path}")
                    
                except Exception as e:
                    print(f"✗ 加载失败 {doc_path}: {e}")
            else:
                print(f"✗ 文件不存在: {doc_path}")
    
    def _load_placeholder(self):
        """占位符加载方法（当PDF库不可用时）"""
        for doc_path in self.document_paths:
            self.documents[doc_path] = {
                'path': doc_path,
                'pages': [],
                'total_pages': 0
            }
            print(f"⚠ 占位符模式: {doc_path}")
    
    def search_in_documents(self, query: str, case_sensitive: bool = False) -> List[Dict]:
        """
        在所有文件中搜索关键词
        
        Args:
            query: 搜索关键词
            case_sensitive: 是否区分大小写
            
        Returns:
            搜索结果列表，包含文件名、页码、匹配文本和上下文
        """
        results = []
        
        # 从配置获取上下文长度
        context_chars = self.config.get("search_settings", {}).get("default_context_chars", 100)
        
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.compile(re.escape(query), flags)
        
        for doc_path, doc_data in self.documents.items():
            for page_data in doc_data['pages']:
                page_num = page_data['page']
                text = page_data['text']
                
                # 查找所有匹配
                matches = pattern.finditer(text)
                
                for match in matches:
                    start = match.start()
                    end = match.end()
                    
                    # 提取上下文（使用配置的长度）
                    context_start = max(0, start - context_chars)
                    context_end = min(len(text), end + context_chars)
                    context = text[context_start:context_end]
                    
                    # 获取匹配所在的段落
                    paragraph = self._extract_paragraph(text, start)
                    
                    results.append({
                        'document': os.path.basename(doc_path),
                        'page': page_num,
                        'match': text[start:end],
                        'context': context.strip(),
                        'paragraph': paragraph.strip(),
                        'position': start
                    })
        
        return results
    
    def _extract_paragraph(self, text: str, position: int) -> str:
        """提取包含指定位置的段落"""
        # 向前查找段落开始（换行符）
        start = text.rfind('\n\n', 0, position)
        if start == -1:
            start = 0
        
        # 向后查找段落结束（换行符）
        end = text.find('\n\n', position)
        if end == -1:
            end = len(text)
        
        return text[start:end]
    
    def search_by_keywords(self, keywords: List[str]) -> Dict:
        """
        使用多个关键词搜索
        
        Args:
            keywords: 关键词列表
            
        Returns:
            按关键词分组的搜索结果
        """
        results = {}
        
        for keyword in keywords:
            results[keyword] = self.search_in_documents(keyword)
        
        return results
    
    def analyze(self, question: str) -> str:
        """
        分析问题并返回基于文件内容的答案
        
        Args:
            question: 用户问题
            
        Returns:
            结构化的答案，包含引用
        """
        # 提取问题中的关键词
        keywords = self._extract_keywords(question)
        
        # 搜索相关内容
        search_results = self.search_by_keywords(keywords)
        
        # 构建答案
        answer = self._build_answer(question, search_results)
        
        return answer
    
    def _extract_keywords(self, question: str) -> List[str]:
        """
        从问题中提取关键词
        
        注意：这是简化版本，实际实现可能需要更复杂的NLP处理
        """
        # 移除常见的疑问词和助词
        stop_words = ['什么', '如何', '怎么', '为什么', '是否', '吗', '呢', '的', '了', '在', '有']
        
        # 简单分词（实际应用中可以使用jieba等分词工具）
        words = []
        for char_group in re.findall(r'[\u4e00-\u9fff]+', question):
            # 移除停用词
            if char_group not in stop_words and len(char_group) >= 2:
                words.append(char_group)
        
        return words[:5]  # 返回前5个关键词
    
    def _build_answer(self, question: str, search_results: Dict) -> str:
        """
        构建结构化答案
        
        Args:
            question: 原始问题
            search_results: 搜索结果
            
        Returns:
            格式化的答案字符串
        """
        answer_parts = []
        
        answer_parts.append("=" * 60)
        answer_parts.append(f"问题：{question}")
        answer_parts.append("=" * 60)
        answer_parts.append("")
        
        # 统计找到的证据
        total_matches = sum(len(results) for results in search_results.values())
        
        if total_matches == 0:
            answer_parts.append("【分析结果】")
            answer_parts.append("根据所提供的三份文件，无法找到与该问题直接相关的信息。")
            answer_parts.append("")
            answer_parts.append("【说明】")
            answer_parts.append("本系统严格遵守'零推测原则'，仅基于文件明确内容提供答案。")
            answer_parts.append("建议：")
            answer_parts.append("1. 尝试使用不同的关键词重新提问")
            answer_parts.append("2. 确认问题是否在这三份文件的范围内")
            answer_parts.append("3. 直接查阅相关章节的完整内容")
        else:
            answer_parts.append("【详细证据】")
            answer_parts.append(f"在三份文件中共找到 {total_matches} 处相关内容：")
            answer_parts.append("")
            
            # 按文档分组显示结果
            evidence_num = 1
            for keyword, results in search_results.items():
                if results:
                    answer_parts.append(f"关键词：{keyword}")
                    answer_parts.append("-" * 60)
                    
                    # 从配置获取最大显示数量
                    max_per_keyword = self.config.get("answer_format", {}).get("max_evidence_per_keyword", 3)
                    max_paragraph_chars = self.config.get("answer_format", {}).get("max_paragraph_chars", 200)
                    
                    for result in results[:max_per_keyword]:  # 使用配置的最大值
                        answer_parts.append(f"{evidence_num}. 【{result['document']}：第{result['page']}页】")
                        answer_parts.append(f"   原文片段：")
                        answer_parts.append(f"   \"{result['paragraph'][:max_paragraph_chars]}...\"")
                        answer_parts.append("")
                        evidence_num += 1
            
            answer_parts.append("【使用说明】")
            answer_parts.append("1. 以上所有内容均直接引用自原文件")
            answer_parts.append("2. 建议查阅完整文件以获取更全面的信息")
            answer_parts.append("3. 如需要更详细的内容，请指定具体的文件和章节")
        
        answer_parts.append("")
        answer_parts.append("=" * 60)
        
        return "\n".join(answer_parts)
    
    def get_document_info(self) -> Dict:
        """获取已加载文档的信息"""
        info = {}
        
        for doc_path, doc_data in self.documents.items():
            info[doc_path] = {
                '文件名': os.path.basename(doc_path),
                '总页数': doc_data['total_pages'],
                '状态': '已加载' if doc_data['total_pages'] > 0 else '未加载'
            }
        
        return info
    
    def export_results(self, results: List[Dict], output_file: str = 'analysis_results.json'):
        """
        导出分析结果到JSON文件
        
        Args:
            results: 分析结果
            output_file: 输出文件路径
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 结果已导出到: {output_file}")


def main():
    """主函数 - 交互式使用"""
    print("=" * 60)
    print("文件内容分析专家系统")
    print("=" * 60)
    print()
    
    # 初始化分析器
    analyzer = DocumentAnalyzer()
    
    print("正在加载文件...")
    analyzer.load_documents()
    print()
    
    # 显示文档信息
    doc_info = analyzer.get_document_info()
    print("已加载的文件：")
    for path, info in doc_info.items():
        print(f"  • {info['文件名']} - {info['总页数']}页 - {info['状态']}")
    print()
    
    # 交互式问答
    print("请输入您的问题（输入'退出'或'quit'结束）：")
    print()
    
    while True:
        try:
            question = input("问题> ").strip()
            
            if question.lower() in ['退出', 'quit', 'exit', 'q']:
                print("感谢使用文件内容分析专家系统！")
                break
            
            if not question:
                continue
            
            print()
            answer = analyzer.analyze(question)
            print(answer)
            print()
            
        except KeyboardInterrupt:
            print("\n\n感谢使用文件内容分析专家系统！")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    main()
