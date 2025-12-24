# 快速开始指南

## 安装

### 1. 克隆或下载项目

```bash
git clone https://github.com/AIbiplayer/Rules.git
cd Rules
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install PyMuPDF
```

## 基本使用

### 方式1: 命令行工具（推荐）

#### 查看文档信息

```bash
python cli.py --info
```

输出：
```
已加载的文档信息
============================================================

1. RoboMaster 2026 机甲大师高校系列赛机器人制作规范手册V1.0.0
   页数: 103
   状态: 已加载

2. RoboMaster 2026 机甲大师高校联盟赛比赛规则手册 V1.1.0
   页数: 80
   状态: 已加载

3. RoboMaster电池安全规范
   页数: 3
   状态: 已加载
```

#### 搜索关键词

```bash
python cli.py --search "机器人尺寸"
```

#### 提问单个问题

```bash
python cli.py --question "电池的安全规范是什么？"
```

#### 交互式模式

```bash
python cli.py
```

然后可以：
- 直接输入问题
- 输入 `search:关键词` 进行搜索
- 输入 `info` 查看文档信息
- 输入 `help` 查看帮助
- 输入 `quit` 退出

#### 批量处理问题

创建问题文件 `questions.txt`：
```
机器人的尺寸限制是什么？
电池有哪些安全要求？
比赛的计分规则是什么？
```

运行批量处理：
```bash
python cli.py --batch questions.txt --output results.json
```

### 方式2: Python脚本

```python
from document_analyzer import DocumentAnalyzer

# 初始化
analyzer = DocumentAnalyzer()
analyzer.load_documents()

# 搜索关键词
results = analyzer.search_in_documents("电池")
for result in results[:3]:
    print(f"{result['document']}, 第{result['page']}页")
    print(result['paragraph'][:100])
    print()

# 回答问题
answer = analyzer.analyze("机器人的尺寸要求是什么？")
print(answer)
```

### 方式3: 直接运行分析器

```bash
python document_analyzer.py
```

进入交互式问答模式。

## 使用技巧

### 1. 提问技巧

**好的问题示例**：
- "机器人的尺寸限制是什么？"
- "电池的充电要求有哪些？"
- "比赛时长是多少？"
- "裁判员的职责是什么？"

**不太好的问题示例**：
- "怎么做？"（太模糊）
- "为什么？"（可能需要推测）
- "最好的方法是什么？"（需要主观判断）

### 2. 搜索技巧

使用具体、专业的关键词：
```bash
# 好的搜索词
python cli.py --search "尺寸限制"
python cli.py --search "功率限制"
python cli.py --search "安全规范"

# 太宽泛的搜索词
python cli.py --search "的"  # 会返回太多结果
```

### 3. 限制搜索结果数量

```bash
python cli.py --search "机器人" --limit 10
```

### 4. 导出结果

```bash
# 导出搜索结果
python cli.py --search "电池" --output battery_info.json

# 导出问答结果
python cli.py --batch questions.txt --output answers.json
```

## 理解系统的核心原则

### ✓ 系统会做什么

1. **基于文件内容回答**
   - 直接引用文件原文
   - 提供精确的页码和位置

2. **搜索相关内容**
   - 在三份文件中全文搜索
   - 返回包含上下文的段落

3. **保持客观中立**
   - 不添加个人观点
   - 不进行主观评价

### ✗ 系统不会做什么

1. **不推测或假设**
   - 如果文件中没有，会明确告知
   - 不会"猜测"答案

2. **不引入外部知识**
   - 仅基于这三份文件
   - 不添加其他来源的信息

3. **不提供建议**
   - 不建议"最佳方案"
   - 不做技术决策

4. **不解释"为什么"**
   - 除非文件中明确说明原因
   - 不推断规则背后的动机

## 常见问题

### Q: 为什么找不到某些信息？

A: 可能的原因：
1. 该信息确实不在这三份文件中
2. 使用的关键词不够准确
3. 信息以不同的表述方式出现

**解决方法**：
- 尝试不同的关键词
- 使用搜索功能查看所有相关段落
- 检查文件目录，查找相关章节

### Q: 系统的回答太简单了？

A: 系统严格遵守"零推测"原则，只提供文件中明确存在的信息。如需更详细的内容：
1. 使用搜索功能查看完整段落
2. 直接阅读相关章节
3. 提出更具体的问题

### Q: 如何验证答案的准确性？

A: 系统提供的每个答案都包含：
- 文件名
- 具体页码
- 原文引用

您可以直接打开PDF文件，跳转到对应页码进行验证。

### Q: 可以分析其他文件吗？

A: 当前系统专门为这三份RoboMaster规则文档设计。如需分析其他文件，需要修改 `document_analyzer.py` 中的 `document_paths` 列表。

### Q: 系统支持哪些功能？

A: 主要功能：
- ✓ 关键词搜索
- ✓ 问答分析
- ✓ 批量处理
- ✓ 结果导出
- ✓ 精确引用
- ✗ 不支持：推测、建议、主观判断

## 高级功能

### 1. 自定义搜索

```python
from document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer()
analyzer.load_documents()

# 多关键词搜索
keywords = ["尺寸", "重量", "功率"]
results = analyzer.search_by_keywords(keywords)

for keyword, matches in results.items():
    print(f"\n{keyword}: {len(matches)} 个匹配")
```

### 2. 导出为JSON

```python
results = analyzer.search_in_documents("电池")
analyzer.export_results(results, "battery_search.json")
```

### 3. 自定义输出格式

可以修改 `document_analyzer.py` 中的 `_build_answer` 方法来自定义输出格式。

## 测试

运行测试脚本验证功能：

```bash
python test_analyzer.py
```

## 更多帮助

- 查看 `README.md` - 完整的系统说明
- 查看 `EXAMPLES.md` - 更多使用示例
- 查看 `SYSTEM_PROMPT.md` - 系统设计原则

## 技术支持

如遇问题，请检查：
1. Python 版本（建议 3.8+）
2. PyMuPDF 是否正确安装
3. PDF 文件是否在正确位置
4. 文件路径是否正确（特别是文件名中的中文字符）

## 贡献

欢迎提出改进建议，但请确保：
1. 保持"零推测"原则
2. 不引入外部知识
3. 保持系统的客观性
