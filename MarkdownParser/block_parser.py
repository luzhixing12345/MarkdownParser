from .base_class import Parser, Handler, Block, CONTAINER
from typing import List
import re
import html


class BlockParser(Parser):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, lines: List[str]):
        self.root = Block(text="")
        if not self.is_sorted:
            self._sort()
            self.is_sorted = True

        for text in lines:
            self.match(self.root, text)
        # self.root.info()
        return self.root

    def match(self, root: Block, text: str):
        for method in self._handlers:
            if method["object"].match(text):
                # print(method['object'].__class__.__name__,'matched')
                method["object"](root, text)
                return


class ComplexBlock(Block):
    # 用于处理复杂嵌套

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)  # pragma: no cover

    def to_html(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()

        return content

    def to_display_word(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_display_word()

        return content

    def to_text(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_text()

        return content

class HTMLBlock(Block):
    # 处理HTML标签
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)  # pragma: no cover

    def __str__(self):
        return "<html>"  # pragma: no cover

    def to_html(self):
        return self.input["text"]


class AnnotateBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self):
        return "<!-->"  # pragma: no cover

    def to_html(self):
        return ""


class EmptyBlockHandler(Handler):
    # 处理空行

    def __init__(self) -> None:
        super().__init__()

    def match(self, text: str):
        return not text.strip()

    def __call__(self, root: Block, text: str):
        root.add_block(EmptyBlock(text=text))


class EmptyBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        return ""


class EscapeCharacterHandler(Handler):
    # preprocess_parser中有着同名方法EscapeCharacterHandler
    # 但修改了其 __call__ 参数

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"\\(.)")

    def sub_func(self, match: re.Match):
        global CONTAINER
        word = match.group(1)
        block = EscapeCharacterBlock(word=word, text="\\" + word)
        replace_name = self.block.register(block)  # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE, self.sub_func, text)
        self.parser.match(self.block, new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block = self.block.sub_blocks[0]
        root.add_block(self.block)


class EscapeCharacterBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.special_characters = [
            "*",
            "[",
            "]",
            "{",
            "}",
            "(",
            ")",
            ".",
            '"',
            "'",
            "\\",
            "`",
            "+",
            "-",
            "<",
            ">",
            "?",
            "/",
            "~",
            "|",
            "!",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            ";",
            ":",
            "_",
        ]

    def to_html(self):
        if self.input["word"] in self.special_characters:
            return self.input["word"]
        else:
            return "\\" + self.input["word"]


class HTMLLabelHandler(Handler):
    # preprocess_parser 中有着同名方法 HTMLLabelHandler
    # 但修改了其 __call__ 参数

    def __init__(self) -> None:
        super().__init__()

        self.RE = re.compile(
            r"""
            (<div[\s\S]*?>[\s\S]*?<\/div>|         # div
            <span[\s\S]*?>[\s\S]*?<\/span>|        # span
            <p[\s\S]*?>[\s\S]*?<\/p>|              # p
            <img[\s\S]*?>(?:<\/img>)?|             # image
            <iframe[\s\S]*?>[\s\S]*?<\/iframe>|    # iframe
            <br\/?>|
            <kbd>[\s\S]*?</kbd>
            )""",
            re.VERBOSE,
        )

    def sub_func(self, match: re.Match):
        global CONTAINER
        src = match.group(0)
        block = HTMLBlock(text=src, word=src)
        return CONTAINER.register(block)

    def __call__(self, root: Block, text: str):
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE, self.sub_func, text)
        self.parser.match(self.block, new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block = self.block.sub_blocks[0]
        root.add_block(self.block)


class ExtensionBlockHandler(Handler):  # pragma: no cover
    # 自定义扩展
    # {% note %}
    # asdklja
    # {%end%}

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(
            r"""(
            (^{[ ]*%[ ]*note[ ]*%[ ]*}[ ]*)|
            (^{[ ]*%[ ]*info[ ]*%[ ]*}[ ]*)|
            (^{[ ]*%[ ]*success[ ]*%[ ]*}[ ]*)|
            (^{[ ]*%[ ]*end[ ]*%[ ]*}[ ]*)
        )""",
            re.VERBOSE,
        )

        self.groupid_tag = {2: "note", 3: "info", 4: "success", 5: "end"}

    def __call__(self, root: Block, text: str):
        match = re.match(self.RE, text)
        # print(match)
        for k, v in self.groupid_tag.items():
            if match.group(k):
                tag = v
                break

        self.block = ExtensionBlock(text=text, tag=tag)
        root.add_block(self.block)


class ExtensionBlock(Block):  # pragma: no cover
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        tag = self.input["tag"]
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()
        return f'<div id="{tag}">{content}</div>'


class SplitBlockHandler(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"^[-=\*]{3,} *$")  # 分隔符

    def __call__(self, root: Block, text: str):
        root.add_block(SplitBlock(text=text))


class SplitBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self):  # pragma: no cover
        return "---<hr>---"

    def to_html(self):
        return "<hr>"


class HierarchyIndentHandler(Handler):
    # 匹配层次缩进
    # - 123
    #   hello world
    #   good luck

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"^([ ]{1,})(.*)")

    def __call__(self, root: Block, text: str):
        match_group = re.match(self.RE, text)
        space_number = len(match_group.group(1))
        word = match_group.group(2)

        self.block = HierarchyBlock(space_number=space_number, text=text)
        root.add_block(self.block)
        self.parser.match(self.block, word)
        # 因为多重 Complex 传递的问题导致的 escape 字符的bug(test8.md)
        # 暂时没有更好的修改方法...
        if len(self.block.sub_blocks) == 1:
            self.block.input["text"] = " " * space_number + self.block.sub_blocks[0].input["text"]


class HierarchyBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()
        return content


class CodeBlockHandler(Handler):
    # 匹配代码段
    # ```python
    # a = 1
    # ```

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"([^`]*?)(`{3,})(.*)")

    def __call__(self, root: Block, text: str):
        match_group = re.search(self.RE, text)
        before_text = match_group.group(1)
        backtick = match_group.group(2)
        language = match_group.group(3).strip()

        if language:
            # 对于多反引号的情况, 在匹配的情况下处理为 SpecialTextBlock
            # https://github.com/luzhixing12345/MarkdownParser/issues/6
            if language.find("`") != -1:
                pattern = re.compile(r"([^`]*?)(`+)")
                special_text_group = re.search(pattern, language)
                word = special_text_group.group(1)
                end_backtick = special_text_group.group(2)
                if end_backtick == backtick:
                    # 反引号数量匹配
                    block = ComplexBlock(text=text)
                    special_text_block = SpecialTextBlock(
                        word=word, tag="highlight", text=f"{backtick}{word}{end_backtick}"
                    )
                    new_text = before_text + pattern.sub(block.register(special_text_block), language)
                    self.parser.match(block, new_text)
                    root.add_block(block)
                else:
                    # 不匹配则以纯文本形式返回
                    root.add_block(TextBlock(word=text, text=text))
            else:
                if before_text.strip() != "":
                    # 奇怪的写法以纯文本形式返回
                    # a```c
                    # int main
                    root.add_block(TextBlock(word=text, text=text))
                else:
                    # 用户可能会在 language 这里添加高亮信息
                    # ```c{3,5}
                    # int main
                    # ```
                    # 将信息提取出来保存在 append_text
                    append_text_group = re.compile(r"{(.*?)}").search(language)
                    append_text = append_text_group.group(1) if append_text_group else None
                    
                    # 去除高亮信息, 更新 language 名字
                    language = re.compile(r"{.*?}").sub("", language).strip()
                    root.add_block(
                        CodeBlock(
                            language=language,
                            text=text,
                            append_text=append_text,
                        )
                    )
        else:
            # 代码段结尾
            root.add_block(CodeBlock(language="UNKNOWN", text=text, append_text=None))


class CodeBlock(Block):
    def __init__(self, **kwargs) -> None:
        # code用于在优化阶段用于整合所有的代码
        super().__init__(code="", **kwargs)

    def to_html(self):
        code = self.input["code"]
        code = html.escape(code)
        language = self.input["language"]
        return f'<pre class="language-{language}"><code>{code}</code></pre>'


class HashHeaderHandler(Handler):
    # 匹配标题
    # ### 123

    def __init__(self) -> None:
        super().__init__()
        # #开头,1-6个#均可 + 一个空格 + 文字
        # Typora               r'(^#{1,6}) (.+)'
        # Markdown All in One  r'(^#{1,6}) (.?)'
        self.RE = re.compile(r"(^#{1,6}) (.+)")

    def __call__(self, root: Block, text: str):
        match_group = re.match(self.RE, text)
        level = len(match_group.group(1))
        header = match_group.group(2).strip()  # 去掉头尾多余空格

        # 继续匹配header中的文字
        block = HashHeaderBlock(level=level, word=header, text=text)
        self.parser.match(block, header)
        root.add_block(block)


class HashHeaderBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.child_blocks = []
        self.parent_block = None
        self.UID = None

    def to_html(self):
        head_level = str(self.input["level"])
        tag = f"h{head_level}"
        if self.UID is not None:
            tag_id = f'id="{tag}-{str(self.UID)}"'
        else:
            tag_id = ""
        return f"<{tag} {tag_id}>{self.sub_blocks[0].to_html()}</{tag}>"

    def to_display_word(self):
        """
        纯文字形式
        """
        word = ""
        for block in self.sub_blocks:
            word += block.to_display_word()
        return word


class TaskListHandler(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"(?<=^[-+\*] )\[([ x])\] (.*)")

    def sub_func(self, match: re.Match):
        is_complete = match.group(1)
        word = match.group(2)

        task_block = TaskListBlock(complete=is_complete, word=word, text=match.group())
        replace_name = self.block.register(task_block)  # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE, self.sub_func, text)
        self.parser.match(self.block, new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block = self.block.sub_blocks[0]
        root.add_block(self.block)


class TaskListBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        checked = "checked" if self.input["complete"] == "x" else ""
        word = self.input["word"]
        return f'<div><input type="checkbox" disabled {checked}>{word}</div>'


class OListHandler(Handler):
    # 匹配有序列表
    # 1. 123
    # 2. 123

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"^(\d+)\. (.*)")

    def __call__(self, root: Block, text: str):
        match_group = re.match(self.RE, text)
        serial_number = match_group.group(1)
        align_space_number = len(serial_number) + 2
        word = match_group.group(2)

        block = OListBlock(serial_number=serial_number, align_space_number=align_space_number, word=word, text=text)
        self.parser.match(block, word)
        root.add_block(block)


class OListBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()
        serial_number = self.input["serial_number"]
        return f'<ol start="{serial_number}"><li>{content}</li></ol>'

    def to_display_word(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_display_word()
        serial_number = self.input["serial_number"]
        return f"{serial_number}. {content}"


class UListHandler(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"^[-+\*] (.*)")

    def __call__(self, root: Block, text: str):
        match_group = re.match(self.RE, text)
        word = match_group.group(1)
        align_space_number = 2

        block = UListBlock(word=word, align_space_number=align_space_number, text=text)
        self.parser.match(block, word)
        root.add_block(block)


class UListBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()

        return f"<ul><li>{content}</li></ul>"


class QuoteHandler(Handler):
    # 匹配引用
    # > 123
    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"^> ?(.*)$")

    def __call__(self, root: Block, text: str):
        match_group = re.match(self.RE, text)
        word = match_group.group(1)
        block = QuoteBlock(word=word, text=text)
        self.parser.match(block, word)
        root.add_block(block)


class QuoteBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()

        return f"<blockquote>{content}</blockquote>"


class PictureHandler(Handler):
    # 匹配图片
    # ![asd](123)

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"!\[([^\!\[\]]*?)\]\((.*?)\)")

    def sub_func(self, match: re.Match):
        word = match.group(1)
        url = match.group(2)
        pic_block = PictureBlock(word=word, url=url, text=match.group())
        replace_name = self.block.register(pic_block)  # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE, self.sub_func, text)

        self.parser.match(self.block, new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block = self.block.sub_blocks[0]

        root.add_block(self.block)


class PictureBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        word = self.input["word"]
        url = self.input["url"]
        return f'<img src="{url}" alt="{word}">'


class ReferenceHandler(Handler):
    # 处理引用
    # [1](abc)

    def __init__(self) -> None:
        super().__init__()
        # 匹配嵌套 + 忽略末尾多余 )

        # Typora               r'\[([^\[\]]*?)\]\((.*?)\)'
        # Markdown All in One  ...

        # https://stackoverflow.com/a/163684/17869889
        web_url_pattern = r"(?:https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;()]+[-A-Za-z0-9+&@#/%=~_|]"

        self.RE = re.compile(
            rf"""(
            \[(.*?)\]\(({web_url_pattern}|.*?)\)|
            <({web_url_pattern})>|
            \b{web_url_pattern}
        )""",
            re.VERBOSE,
        )

    def sub_func(self, match: re.Match):
        word = match.group(2)
        url = match.group(3)

        if url is None:
            # <> 的匹配
            url = match.group(4)
            if url is None:
                # 裸https的情况
                url = match.group(1)
            word = url
        ref_block = ReferenceBlock(word=word, url=url, text=match.group())
        replace_name = self.block.register(ref_block)  # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE, self.sub_func, text)
        self.parser.match(self.block, new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block = self.block.sub_blocks[0]
        root.add_block(self.block)


class ReferenceBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # 默认Markdown启用的是_self, 这里存粹是因为我自己的习惯所以改成 _blank
        self.target = "_blank"
        # self.target = '_self'

    def to_html(self):
        url = self.input["url"]
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()
        return f'<a href="{url}" target="{self.target}">{content}</a>'


class SpecialTextHandler(Handler):
    # 处理特殊字符
    # 不考虑 * 的多级嵌套

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(
            r"""(
            ``(?P<highlight1>.+?)``|
            `(?P<highlight2>.+?)`|                                 # 高亮
            \*{3}(?P<bold_italics>[^ ][^`]*?)\*{3}|           # 粗体+斜体
            \*{2}(?P<bold>[^ ][^`]*?)\*{2}|                   # 粗体
            \*(?P<italic>[^ ][^`]*?)\*|                       # 斜体
            ~~(?P<delete>[^`]+?)~~                                # 删除线
        )""",
            re.VERBOSE,
        )

    def sub_func(self, match: re.Match):
        for group_name, group_value in match.groupdict().items():
            if group_value is not None:
                word = match.group(group_name)
                tag = group_name
                break

        special_text_block = SpecialTextBlock(word=word, tag=tag, text=match.group())
        replace_name = self.block.register(special_text_block)  # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE, self.sub_func, text)

        self.parser.match(self.block, new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block = self.block.sub_blocks[0]
        root.add_block(self.block)


class SpecialTextBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        tag = self.input["tag"]
        content = ""
        for block in self.sub_blocks:
            content += block.to_html()
        if tag == "bold_italics":
            return f"<i><b>{content}</b></i>"
        elif tag == "bold":
            return f"<b>{content}</b>"
        elif tag == "italic":
            return f"<i>{content}</i>"
        elif tag == "delete":
            return f"<del>{content}</del>"
        elif tag.startswith("highlight"):
            return f"<code>{content}</code>"
        else:  # pragma: no cover
            raise ValueError(f"unknown tag {tag}")

    def to_display_word(self):
        content = ""
        for block in self.sub_blocks:
            content += block.to_display_word()
        return content

    def to_text(self): # pragma: no cover
        content = ""
        for block in self.sub_blocks:
            content += block.to_text()
            
        tag = self.input["tag"]
        if tag == "bold_italics":
            return f"***{content}***"
        elif tag == "bold":
            return f"**{content}**"
        elif tag == "italic":
            return f"*{content}*"
        elif tag == "delete":
            return f"~~{content}~~"
        elif tag == "highlight1":
            return f"``{content}``"
        elif tag == "highlight2":
            return f"`{content}`"
        else:  # pragma: no cover
            raise ValueError(f"unknown tag {tag}")


class TableHandler(Handler):
    # 处理表格
    # 不想支持原生表格...

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r"^\|(?: *:?-{1,}:? *\|)+")  # 判断表格出现

    def __call__(self, root: Block, text: str):
        # 判断对齐方式
        lines = text.split("|")[1:-1]
        alignments = []
        for line in lines:
            if re.search(r":-+:", line):
                alignments.append("center")
            elif re.search(r"-:", line):
                alignments.append("right")
            else:
                alignments.append("left")
        root.add_block(TableBlock(text=text, alignments=alignments))


class TableBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # self.input['header'] 表格头节点
        # self.input['alignments'] 表格对齐方式
        # self.input['length'] 表格列数
        # self.input['table_items'] 每一行的表格项(Block)

    def add_table_item(self, block: Block):
        # 将一个table表项添加到Block中
        self.sub_blocks.extend(block.sub_blocks)

    def to_html(self):
        alignments = self.input["alignments"]

        table_header_content = "<tr>"
        for block in self.input["header"].sub_blocks:
            table_header_content += f"<th>{block.to_html()}</th>"
        table_header_content += "</tr>"

        table_items_content = ""
        for i in range(len(self.sub_blocks)):
            if i % len(alignments) == 0:
                table_items_content += "<tr>"
            align_style = alignments[i % len(alignments)]
            table_items_content += f'<td style="text-align:{align_style}">\
                {self.sub_blocks[i].to_html()}</td>'
            if (i + 1) % len(alignments) == 0:
                table_items_content += "</tr>"

        return f"<table>{table_header_content}{table_items_content}</table>"


class TextHandler(Handler):
    # 处理常规文本

    def __init__(self) -> None:
        super().__init__()

    def match(self, text: str):
        return True

    def __call__(self, root: Block, text: str):
        global CONTAINER
        RE = re.compile(r"({-%.*?%-})")
        split_strings = RE.split(text.strip())

        count = 0
        temp_block = ComplexBlock(text=text)

        for string in split_strings:
            # 正常文本字符
            if count % 2 == 0:
                if string:
                    temp_block.add_block(TextBlock(word=string, text=string))
            else:
                id = string[3:-3]
                class_object: Block = CONTAINER[id]
                replace_str = class_object.input["text"]
                if class_object is not None:
                    class_object.restore(TextBlock)
                    temp_block.input["text"] = temp_block.input["text"].replace(string, replace_str)
                    root.input["text"] = root.input["text"].replace(string, replace_str)
                    temp_block.add_block(class_object)
                else:
                    # 由于在解析过程中中间变量使用了{-%.*?%-}的格式进行代替
                    # 所以如果原本的Markdown输入中就包含类似的 {-%asdjkl%-}文字则会出现无法找到的情况
                    temp_block.add_block(TextBlock(word=string, text=string))  # pragma: no cover
            count += 1

        if len(temp_block.sub_blocks) <= 1:
            root.add_block(temp_block.sub_blocks[0])
        else:
            root.add_block(temp_block)


class TextBlock(Block):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_html(self):
        # fix bug: 修复一些 <abc> 这种虽然不匹配网址, 但是会被 html 解析为标签的情况
        # 见 test14.md
        self.input["word"] = html.escape(self.input["word"])
        return self.input["word"]


def build_block_parser():
    # block parser 用于逐行处理文本, 并将结果解析为一颗未优化的树
    block_parser = BlockParser()
    block_parser.register(EmptyBlockHandler(), 100)
    block_parser.register(EscapeCharacterHandler(), 98)
    block_parser.register(SplitBlockHandler(), 95)
    block_parser.register(HierarchyIndentHandler(), 90)
    block_parser.register(HashHeaderHandler(), 80)
    block_parser.register(TaskListHandler(), 70)
    block_parser.register(OListHandler(), 60)
    block_parser.register(UListHandler(), 50)
    block_parser.register(QuoteHandler(), 40)
    block_parser.register(CodeBlockHandler(), 30)
    block_parser.register(PictureHandler(), 15)
    block_parser.register(ReferenceHandler(), 10)
    block_parser.register(SpecialTextHandler(), 5)
    block_parser.register(TableHandler(), 4)
    block_parser.register(TextHandler(), 0)
    return block_parser
