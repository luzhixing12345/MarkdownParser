

from .preprocess_parser import buildPreprocessParser
from .block_parser import buildBlockParser
from .tree_parser import buildTreeParser


class Markdown:
    def __init__(self) -> None:
        self.build_parser()

    def build_parser(self):

        self.preprocess_parser = buildPreprocessParser()
        self.block_parser = buildBlockParser()
        self.tree_parser = buildTreeParser()

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


def parse(text: str) -> str:

    assert type(text) == str, "输入应为字符串"

    # 空输入
    if not text.strip():
        return ''

    md = Markdown()
    return md.parse(text)


def parseFile(file_name: str) -> str:

    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()

    return parse(text)
