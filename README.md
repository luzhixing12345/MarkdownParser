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

接口类

- `Markdown`

  使用类创建对象后可以利用 `self.preprocess_parser` `self.block_parser` `self.tree_parser` 控制解析过程

  其中Block类属性见[base_class.py](MarkdownParser/base_class.py),可以通过调用block.info()函数查看树的结构

  tree可以通过内部toHTML()方法得到HTML元素

## 不支持

- 四个空格变为代码段(不想支持)
- [^1]的引用方式(不想支持)
- Latex数学公式(不会支持)
- Setext 形式的标题(不想支持)
- 上标 / 下标 / 下划线(不想支持)
- SpecialTextBlock中叠加使用有可能会有bug(没想好怎么支持)
- TOC与锚点(暂不支持)

  锚点的添加通常和目录的跳转有关,而目录树的生成可以考虑解析tree的根Block的所有子HashHeaderBlock来构建.
  
  因为跳转的功能是js实现,锚点id的加入也会影响html结构,所以暂不支持

## 其他特性

- 最外层为div包裹,类名为 `markdown-body`
- 代码段会根据语言加入一个类名便于后期高亮 `class="language-cpp"`, 未定义语言则为 `language-UNKNOWN`
- 列表嵌套稍有不同,ul/ol+li完全体

## 相关参考

- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)
- [Mermaid API](https://mermaid.js.org/intro/#mermaid-api)