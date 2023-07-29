from .base_class import Parser, Handler
import re
from .block_parser import HTMLBlock, EscapeCharacterBlock, AnnotateBlock
from .base_class import CONTAINER


class PreprocessParser(Parser):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, data: str):
        self._sort()
        # 按优先级逐步执行相应处理方法
        for method in self._handlers:
            data = method["object"](data)

        lines = data.split("\n")
        return lines


class TabHandler(Handler):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, text: str):
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = text.expandtabs(tabsize=4)

        return text


class EscapeCharacterHandler(Handler):
    # 处理转义字符

    def __init__(self) -> None:
        super().__init__()

    def sub_func(self, match: re.Match):
        global CONTAINER
        word = match.group(1)
        block = EscapeCharacterBlock(word=word, text="\\" + word)
        return CONTAINER.register(block)

    def __call__(self, text: str):
        text = re.sub(r"\\(.)", self.sub_func, text)
        return text


class AnnotateHandler(Handler):
    # 去除注释

    def __init__(self) -> None:
        super().__init__()

    def sub_func(self, match: re.Match):
        global CONTAINER
        word = match.group()
        block = AnnotateBlock(word=word, text=word)
        return CONTAINER.register(block)

    def __call__(self, text: str):
        text = re.sub(r"\<!--[\s\S]*?--\>", self.sub_func, text)  # 去除注释
        return text


class HTMLLabelHandler(Handler):
    # TODO: 标签不自闭合的处理

    def __init__(self) -> None:
        super().__init__()

        self.RE = re.compile(
            r"""
            (<div[\s\S]*?>[\s\S]*?<\/div>|         # div
            <span[\s\S]*?>[\s\S]*?<\/span>|        # span
            <p[\s\S]*?>[\s\S]*?<\/p>|            # p
            <img[\s\S]*?>(?:<\/img>)?|   # image
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

    def __call__(self, text: str):
        text = re.sub(self.RE, self.sub_func, text)
        text = re.sub(r"^[\n]+", "", text)  # 去除开头连续空换行
        # text = re.sub(r'[\n]+$', '', text)                    # 去除结尾连续空换行
        # text = re.sub(r'[\n]{3,}', '\n\n', text)              # 去除连续换行
        # print(text)
        return text


def build_preprocess_parser():
    # preprocess parser 用于预处理空行/注释/HTML标签
    preprocess_parser = PreprocessParser()
    preprocess_parser.register(TabHandler(), priority=100)
    preprocess_parser.register(EscapeCharacterHandler(), priority=90)
    preprocess_parser.register(AnnotateHandler(), priority=85)
    preprocess_parser.register(HTMLLabelHandler(), priority=80)
    return preprocess_parser
