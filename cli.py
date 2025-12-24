#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行工具 - 文件内容分析专家系统
提供便捷的命令行接口进行文档分析
"""

import argparse
import sys
import json
from document_analyzer import DocumentAnalyzer


def main():
    """主函数 - 命令行接口"""
    parser = argparse.ArgumentParser(
        description='文件内容分析专家系统 - 基于三份RoboMaster规则文档的分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 交互式问答
  python cli.py

  # 搜索关键词
  python cli.py --search "电池安全"

  # 回答单个问题
  python cli.py --question "机器人的尺寸限制是什么？"

  # 批量处理问题
  python cli.py --batch questions.txt

  # 显示文档信息
  python cli.py --info

  # 导出搜索结果
  python cli.py --search "规范" --output results.json
        """
    )

    parser.add_argument(
        '--search', '-s',
        metavar='KEYWORD',
        help='搜索指定关键词'
    )

    parser.add_argument(
        '--question', '-q',
        metavar='QUESTION',
        help='回答单个问题'
    )

    parser.add_argument(
        '--batch', '-b',
        metavar='FILE',
        help='批量处理问题（每行一个问题）'
    )

    parser.add_argument(
        '--info', '-i',
        action='store_true',
        help='显示已加载文档的信息'
    )

    parser.add_argument(
        '--output', '-o',
        metavar='FILE',
        help='输出结果到JSON文件'
    )

    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=5,
        metavar='N',
        help='限制搜索结果数量（默认：5）'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )

    args = parser.parse_args()

    # 初始化分析器
    print("正在初始化文件内容分析专家系统...")
    analyzer = DocumentAnalyzer()
    
    if args.verbose:
        print("正在加载文档...")
    
    analyzer.load_documents()

    if args.verbose:
        print("文档加载完成\n")

    # 处理不同的命令
    if args.info:
        show_info(analyzer)
    
    elif args.search:
        search_keyword(analyzer, args.search, args.limit, args.output)
    
    elif args.question:
        answer_question(analyzer, args.question)
    
    elif args.batch:
        batch_process(analyzer, args.batch, args.output)
    
    else:
        # 默认进入交互模式
        interactive_mode(analyzer)


def show_info(analyzer):
    """显示文档信息"""
    print("=" * 60)
    print("已加载的文档信息")
    print("=" * 60)
    print()
    
    info = analyzer.get_document_info()
    for idx, (path, details) in enumerate(info.items(), 1):
        print(f"{idx}. {details['文件名']}")
        print(f"   页数: {details['总页数']}")
        print(f"   状态: {details['状态']}")
        print()


def search_keyword(analyzer, keyword, limit, output_file):
    """搜索关键词"""
    print("=" * 60)
    print(f"搜索关键词: {keyword}")
    print("=" * 60)
    print()
    
    results = analyzer.search_in_documents(keyword)
    
    print(f"找到 {len(results)} 处匹配\n")
    
    if results:
        display_count = min(limit, len(results))
        print(f"显示前 {display_count} 个结果：\n")
        
        for idx, result in enumerate(results[:display_count], 1):
            print(f"{idx}. 【{result['document']}：第{result['page']}页】")
            print(f"   {result['paragraph'][:150]}...")
            print()
        
        if len(results) > limit:
            print(f"... 还有 {len(results) - limit} 个结果未显示")
    
    # 导出结果
    if output_file:
        analyzer.export_results(results, output_file)


def answer_question(analyzer, question):
    """回答单个问题"""
    answer = analyzer.analyze(question)
    print(answer)


def batch_process(analyzer, input_file, output_file):
    """批量处理问题"""
    print("=" * 60)
    print(f"批量处理问题: {input_file}")
    print("=" * 60)
    print()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            questions = [line.strip() for line in f if line.strip()]
        
        print(f"共 {len(questions)} 个问题\n")
        
        results = []
        for idx, question in enumerate(questions, 1):
            print(f"处理问题 {idx}/{len(questions)}: {question}")
            answer = analyzer.analyze(question)
            
            results.append({
                'question': question,
                'answer': answer
            })
            
            print(f"✓ 完成\n")
        
        # 导出结果
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✓ 结果已导出到: {output_file}")
        else:
            # 显示所有结果
            for result in results:
                print(result['answer'])
                print()
    
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


def interactive_mode(analyzer):
    """交互式问答模式"""
    print("=" * 60)
    print("文件内容分析专家系统 - 交互模式")
    print("=" * 60)
    print()
    print("已加载的文档：")
    
    info = analyzer.get_document_info()
    for details in info.values():
        print(f"  • {details['文件名']} ({details['总页数']}页)")
    
    print()
    print("命令说明：")
    print("  - 输入问题进行分析")
    print("  - 输入 'search:关键词' 进行搜索")
    print("  - 输入 'info' 查看文档信息")
    print("  - 输入 'help' 查看帮助")
    print("  - 输入 'quit' 或 'exit' 退出")
    print()
    
    while True:
        try:
            user_input = input(">>> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print("\n感谢使用文件内容分析专家系统！")
                break
            
            elif user_input.lower() == 'help':
                show_help()
            
            elif user_input.lower() == 'info':
                show_info(analyzer)
            
            elif user_input.lower().startswith('search:'):
                keyword = user_input[7:].strip()
                if keyword:
                    search_keyword(analyzer, keyword, 5, None)
                else:
                    print("请提供搜索关键词")
            
            else:
                # 作为问题处理
                print()
                answer = analyzer.analyze(user_input)
                print(answer)
                print()
        
        except KeyboardInterrupt:
            print("\n\n感谢使用文件内容分析专家系统！")
            break
        except Exception as e:
            print(f"错误: {e}")


def show_help():
    """显示帮助信息"""
    print()
    print("=" * 60)
    print("帮助信息")
    print("=" * 60)
    print()
    print("交互模式命令：")
    print("  1. 直接输入问题 - 系统会基于文件内容回答")
    print("     示例: 机器人的尺寸限制是什么？")
    print()
    print("  2. search:关键词 - 搜索包含关键词的所有段落")
    print("     示例: search:电池")
    print()
    print("  3. info - 显示已加载文档的信息")
    print()
    print("  4. help - 显示此帮助信息")
    print()
    print("  5. quit/exit - 退出系统")
    print()
    print("系统特点：")
    print("  • 严格依据文件原文，绝不推测")
    print("  • 提供精确的文件引用和页码")
    print("  • 保持客观中立，不添加外部知识")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
        sys.exit(0)
