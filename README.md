# MarkdownParser

MarkdownParser 是一个 Markdown 语法解析器,用于实现md到html标签的转换

## 安装

```bash
pip install markdownparser
```

## 快速使用

```python
import MarkdownParser

html = MarkdownParser.parse('# Hello World')
print(html)

#<div class='markdown-body'><h1>Hello World!</h1></div>
```

## 不支持

- 四个空格变为代码段
- [^1]的引用方式
- Latex数学公式
- Setext 形式的标题
- 上标 / 下标 / 下划线
- SpecialTextBlock中叠加使用有可能会有bug

## 相关参考

- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)