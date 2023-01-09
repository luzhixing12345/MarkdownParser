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

其他接口函数

- `parseFile(file_name:str)->str`: 解析文件
- `parseToRoot(text:str)->Block`: 逐行解析,得到一颗未优化的树
- `parseToTree(text:str)->Block`: 优化,得到正确的markdown解析树

其中Block类属性见'base_class.py`,可以通过print打印查看

接口类

- `Markdown`

## 不支持

- 四个空格变为代码段(不想支持)
- [^1]的引用方式(不想支持)
- Latex数学公式(不会支持)
- Setext 形式的标题(不想支持)
- 上标 / 下标 / 下划线(不想支持)
- SpecialTextBlock中叠加使用有可能会有bug(没想好怎么支持)

## 其他特性

- 最外层为div包裹,类名为 `markdown-body`
- 代码段会根据语言加入一个类名便于后期高亮 `class="language-cpp"`, 未定义语言则为 `language-UNKNOWN`
- 列表嵌套稍有不同,ul/ol+li完全体

## 相关参考

- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)