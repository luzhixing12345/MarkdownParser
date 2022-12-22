# MarkdownParser

Markdown 语法解析器

## 使用

```bash
python main.py
```

使用的markdown文件为[test.md](testfiles/test.md)

渲染结果:

![20221219174226](https://raw.githubusercontent.com/learner-lu/picbed/master/20221219174226.png)

## 不支持

- 四个空格变为代码段
- [^1]的引用方式
- Latex数学公式
- Setext 形式的标题
- 上标 / 下标 / 下划线
- SpecialTextBlock中叠加使用有可能会有bug

## 相关参考

- [Github Markdown CSS](https://cdn.jsdelivr.net/npm/github-markdown-css@4.0.0/github-markdown.css)