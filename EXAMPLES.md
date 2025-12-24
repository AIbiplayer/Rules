# 使用示例

## 示例 1: 基本使用

```python
from document_analyzer import DocumentAnalyzer

# 创建分析器实例
analyzer = DocumentAnalyzer()

# 加载三份文件
analyzer.load_documents()

# 提出问题
question = "机器人的尺寸限制是什么？"
answer = analyzer.analyze(question)
print(answer)
```

## 示例 2: 搜索特定关键词

```python
from document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()
analyzer.load_documents()

# 搜索单个关键词
results = analyzer.search_in_documents("电池")

# 显示结果
for result in results:
    print(f"文件: {result['document']}")
    print(f"页码: {result['page']}")
    print(f"内容: {result['paragraph'][:100]}...")
    print("-" * 40)
```

## 示例 3: 多关键词搜索

```python
from document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()
analyzer.load_documents()

# 搜索多个关键词
keywords = ["机器人", "尺寸", "重量"]
results = analyzer.search_by_keywords(keywords)

# 按关键词查看结果
for keyword, matches in results.items():
    print(f"\n关键词: {keyword}")
    print(f"找到 {len(matches)} 处匹配")
    for match in matches[:3]:  # 显示前3个
        print(f"  - {match['document']}, 第{match['page']}页")
```

## 示例 4: 导出结果

```python
from document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()
analyzer.load_documents()

# 搜索并导出结果
results = analyzer.search_in_documents("安全规范")
analyzer.export_results(results, "safety_rules.json")
```

## 示例 5: 查看文档信息

```python
from document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()
analyzer.load_documents()

# 获取文档信息
info = analyzer.get_document_info()
for path, details in info.items():
    print(f"文件: {details['文件名']}")
    print(f"页数: {details['总页数']}")
    print(f"状态: {details['状态']}")
    print()
```

## 常见问题示例

### 问题1: 机器人制作规范相关
```python
questions = [
    "机器人的最大尺寸是多少？",
    "机器人允许使用什么类型的电池？",
    "机器人的重量限制是什么？"
]

for q in questions:
    print(analyzer.analyze(q))
```

### 问题2: 比赛规则相关
```python
questions = [
    "比赛的计分规则是什么？",
    "比赛时长是多少？",
    "参赛队伍有什么要求？"
]

for q in questions:
    print(analyzer.analyze(q))
```

### 问题3: 电池安全相关
```python
questions = [
    "电池的充电要求是什么？",
    "电池的存储规范是什么？",
    "电池使用有哪些安全注意事项？"
]

for q in questions:
    print(analyzer.analyze(q))
```

## 交互式使用

直接运行脚本进入交互模式：

```bash
python document_analyzer.py
```

然后输入问题：

```
问题> 机器人的电池要求是什么？
```

系统会返回：
- 详细证据（包含文件名和页码）
- 原文引用
- 相关补充信息

## 命令行参数（可扩展）

```bash
# 基本用法
python document_analyzer.py

# 搜索特定关键词
python document_analyzer.py --search "电池安全"

# 批量处理问题
python document_analyzer.py --questions questions.txt

# 导出结果
python document_analyzer.py --output results.json
```

## 注意事项

1. **首次使用需要安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **确保PDF文件在正确位置**：
   - 三个PDF文件应该在与脚本相同的目录下

3. **搜索技巧**：
   - 使用具体的关键词
   - 可以使用专业术语
   - 避免过于模糊的问题

4. **理解限制**：
   - 系统只回答文件中明确存在的内容
   - 不会进行推测或补充外部知识
   - 如果找不到信息，会明确告知

## 高级用法

### 自定义搜索范围

```python
# 只搜索特定文档
analyzer = DocumentAnalyzer()
analyzer.document_paths = [
    "RoboMaster 2026 机甲大师高校联盟赛比赛规则手册 V1.1.0（20251208）.pdf"
]
analyzer.load_documents()
```

### 批量处理问题

```python
import json

# 从文件读取问题列表
with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 批量分析
results = []
for question in questions:
    answer = analyzer.analyze(question)
    results.append({
        'question': question,
        'answer': answer
    })

# 保存结果
with open('batch_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```
