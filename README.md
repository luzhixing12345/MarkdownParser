# MarkdownParser

Markdown 语法解析器

## 使用

```bash
python main.py
```

## 示例

```Markdown
# Head1

## [Head2](跳转到这里)

![图片下的文字](图片地址)

Hello World!

> 这是一个注释
> 它们应该在一起

> 这是一个单独的注释

1. 有序列表
2. 第二个有序列表

- 搞一个无序列表试试看?
- 说不定可以
- 大概可以..

或许我们可以支持**使用\*来强调**,或者试试*斜体?*

```c
#include <iostream>
int main(int argc,char**argv) {
    std::cout << "markdown怎么能少了代码段呢?" << std::endl;
    return 0;
}
```1
```

```html
<h1>Head1</h1>
<h2><a href="跳转到这里">Head2</a></h2>
<p><img alt="图片下的文字" src="图片地址" /></p>
<p>Hello World!</p>
<blockquote>
<p>这是一个注释
它们应该在一起</p>
<p>这是一个单独的注释</p>
</blockquote>
<ol>
<li>有序列表</li>
<li>
<p>第二个有序列表</p>
</li>
<li>
<p>搞一个无序列表试试看?</p>
</li>
<li>说不定可以</li>
<li>大概可以..</li>
</ol>
<p>或许我们可以支持<strong>使用*来强调</strong>,或者试试<em>斜体?</em></p>
<p>```c</p>
<h1>include <iostream></h1>
<p>int main(int argc,char**argv) {
    std::cout &lt;&lt; "markdown怎么能少了代码段呢?" &lt;&lt; std::endl;
    return 0;
}
```</p>
```