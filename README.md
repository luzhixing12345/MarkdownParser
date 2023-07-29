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

接口函数

```python
# 解析 markdown 文本转 html
def parse(text: str) -> str:

# 解析 md 文件转 html
def parse_file(file_name: str) -> str:

# 解析 markdown 文本, 带目录树
def parse_toc(text: str) -> str:

# 解析 md 文件, 带目录树
def parse_file_toc(file_name: str) -> str:
```

接口类 Markdown, Block

## 结果预览与 Markdown 功能测试

本仓库下提供了了一个快速验证转换结果的工具 generate.py

```bash
python generate.py <FILE_NAME>

# python generate.py ./testfiles/test1.md
# python generate.py README.md
```

运行会生成index.html, 使用浏览器打开生成的index.html即可与您预期的渲染结果对比, README 的渲染结果如下所示

![20230218202400](https://raw.githubusercontent.com/learner-lu/picbed/master/20230218202400.png)

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
- `<details><summary></summary></details>` 折叠块

## HTML 结果说明

- 生成的结果如下 `<div class='markdown-body'>markdown内容</div>`
- 代码段会根据语言为 pre 加入一个类名便于后期高亮,例如 `class="language-cpp"`, 未定义语言则为 `language-UNKNOWN`
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

- 您可以使用 `parse_toc` 将 HashHeadBlock 提取出来组成目录树, 得到一个 `<div class="header-navigator">...</div>` 并添加到返回的 HTML 元素中, 您可能还需要一些 js 相关的代码实现跳转, 具体可以参考 [template.html](./template.html)

  ```js
  let links = document.querySelectorAll('div a[href^="#"]');
    links.forEach(link => {
      link.addEventListener('click', function(event) {
        event.preventDefault();
        let target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth' });
      });
    });
  ```

  以及一些样式美化

  ```css
  .header-navigator {
    position: fixed;
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

  注意,这里仅支持很少一部分数学公式

## 参考

- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)
- [Mermaid API](https://mermaid.js.org/intro/#mermaid-api)
- [MathJax](https://docs.mathjax.org/en/latest/web/start.html)