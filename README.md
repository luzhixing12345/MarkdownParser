# MarkdownParser

[![codecov](https://codecov.io/gh/luzhixing12345/MarkdownParser/branch/main/graph/badge.svg?)](https://codecov.io/gh/luzhixing12345/MarkdownParser)

MarkdownParser 是一个 Markdown 语法解析器,用于实现md到html标签的转换

## 安装

```bash
pip install markdownparser
```

## 快速使用

```python
import MarkdownParser

html = MarkdownParser.parse('# Hello World!')
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

## 测试

```bash
python generate.py <FILE_NAME>

# python generate.py ./testfiles/test1.md
# python generate.py README.md
```

运行会生成index.html, 使用浏览器打开生成的index.html即可与您的Markdown编辑器的预期渲染结果对比

![20230218202400](https://raw.githubusercontent.com/learner-lu/picbed/master/20230218202400.png)

代码覆盖率

```bash
coverage run -m unittest
coverage html
```

## 实现思路

[Markdown解析器的代码实现](https://www.bilibili.com/video/BV1LA411X7X3)

您可通过取消 [core.py](./MarkdownParser/core.py) 注释来获取树的结构

```python
def parse(self, text: str) -> str:

    # 去除空行/注释/html标签
    lines = self.preprocess_parser(text)
    # print(lines)
    # 逐行解析,得到一颗未优化的树
    root = self.block_parser(lines)
    # root.info()
    # 优化,得到正确的markdown解析树
    tree = self.tree_parser(root)
    # tree.info()
    # 输出到屏幕 / 导出html文件
    return tree.toHTML()
```

## 不支持

- 四个空格变为代码段
- [^1]的引用方式
- Setext 形式的标题
- 上标 / 下标 / 下划线
- TOC与锚点

  锚点的添加通常和目录的跳转有关,而目录树的生成可以考虑解析tree的根Block的所有子HashHeaderBlock来构建.
  
  因为跳转的功能是js实现,锚点id的加入也会影响html结构,所以暂不支持

## 补充说明

- 生成的结果如下 `<div class='markdown-body'>markdown内容</div>`
- 代码段会根据语言加入一个类名便于后期高亮,例如 `class="language-cpp"`, 未定义语言则为 `language-UNKNOWN`
- 默认导出的HTML中层级任务列表会有显示问题,这是因为使用了ul+li+checkbox的方式,您需要添加以下css样式修正

  ```css
  .markdown-body > ul>li:has(input) {
    padding-left: 0;
    margin-bottom: 0;
  }

  .markdown-body  ul>li:has(input)>ul {
    list-style-type: none;
    padding-left: 8px;
  }
  ```

- 如果您想添加对[Mermaid](https://mermaid.js.org/)的支持, 您可参考[mermaid plugin](https://mermaid.js.org/intro/n00b-gettingStarted.html#_2-using-mermaid-plugins)在您的html页面 `<body>` 末尾添加如下 `<script>`

  ```html
  <script type="module">
    const codeBlocks = document.querySelectorAll('.language-mermaid');
    codeBlocks.forEach(codeBlock => {
        codeBlock.classList.remove('language-mermaid');
        codeBlock.classList.add('mermaid');
    });
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
  ```

  > **请注意**, 由于本Markdown解析器的CodeBlock解析得到的类名为 `language-mermaid`, 而mermaid插件支持的类名格式为`mermaid`, 所以代码中手动修改了 `language-mermaid` 的类名

- 如果您想添加对Latex数学公式的支持, 可以在html页面 `<body>` 末尾添加如下 `<script>`

  ```html
  <script>
      MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']]
        }
      };
      </script>
  <script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
  </script>
  ```

  注意,这里仅支持

## 相关参考

- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)
- [Mermaid API](https://mermaid.js.org/intro/#mermaid-api)
- [MathJax](https://docs.mathjax.org/en/latest/web/start.html)