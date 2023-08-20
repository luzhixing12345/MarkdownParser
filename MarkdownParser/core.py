
import os
from .preprocess_parser import build_preprocess_parser
from .block_parser import build_block_parser, HashHeaderBlock, Block
from .tree_parser import build_tree_parser


class Markdown:
    def __init__(self) -> None:
        self.build_parser()

    def build_parser(self):
        self.preprocess_parser = build_preprocess_parser()
        self.block_parser = build_block_parser()
        self.tree_parser = build_tree_parser()

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
    
    def parse_with_tag(self, text: str):
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
        header_navigater = self.get_toc(tree)
        return tree.toHTML(header_navigater)

    def get_toc(self, tree:Block):
        '''
        tree 为解析的目录树, 返回一个 html 目录树
        '''
        UID = 0
        H0_block = []
        activate_block: HashHeaderBlock = None  # 激活节点
        activate_block_level = 0
        for block in tree.sub_blocks:
            # 对所有 HashHeaderBlock 统计树结构
            if isinstance(block, HashHeaderBlock):
                current_head_level = block.input["level"]
                # 第一次匹配
                if activate_block is None:
                    activate_block = block
                    activate_block_level = current_head_level
                    activate_block.parent_block = None
                    activate_block.UID = UID
                    UID += 1
                    H0_block.append(activate_block)
                else:
                    # 当前 block 是激活节点的子节点
                    if current_head_level > activate_block_level:
                        block.UID = UID
                        UID += 1
                        activate_block.child_blocks.append(block)
                        block.parent_block = activate_block
                        activate_block = block
                        activate_block_level = current_head_level
                    # 当前 block 是激活节点同层级的
                    # 向上一层搜索
                    elif current_head_level == activate_block_level:
                        activate_block = activate_block.parent_block
                        if activate_block is None:
                            block.UID = UID
                            UID += 1
                            H0_block.append(block)
                            block.parent_block = None
                            activate_block = block
                            activate_block_level = current_head_level
                        else:
                            block.UID = UID
                            UID += 1
                            activate_block.child_blocks.append(block)
                            block.parent_block = activate_block
                            activate_block = block
                            activate_block_level = current_head_level
                    # 当前 block 是激活节点高层级的
                    else:
                        # 一直向上找
                        while activate_block_level >= current_head_level:
                            activate_block = activate_block.parent_block
                            if activate_block is None:
                                break
                            activate_block_level = activate_block.input["level"]

                        # 到达根部
                        if activate_block is None:
                            block.UID = UID
                            UID += 1
                            H0_block.append(block)
                            activate_block = block
                            block.parent_block = None
                            activate_block_level = current_head_level
                        # 找到了可以满足层次高于当前 block 的激活节点
                        else:
                            block.UID = UID
                            UID += 1
                            activate_block.child_blocks.append(block)
                            block.parent_block = activate_block
                            activate_block = block
                            activate_block_level = current_head_level

        return self.get_header_navigator(H0_block)

    def get_header_navigator(self, H0_block):
        navigator_html = ""
        for block in H0_block:
            navigator_html += self._get_header_navigator(block)
        navigator_html = f'<div class="header-navigator">{navigator_html}</div>'
        return navigator_html

    def _get_header_navigator(self, block: HashHeaderBlock):
        navigator_html = ""
        level = block.input["level"]
        tag = f"h{str(level)}-{str(block.UID)}"
        word = block.to_href()
        if len(block.child_blocks) == 0:
            navigator_html = f'<ul><li><a href="#{tag}">{word}</a></li></ul>'
        else:
            sub_navigator_html = ""
            for cblock in block.child_blocks:
                sub_navigator_html += self._get_header_navigator(cblock)
            navigator_html = f'<ul><li><a href="#{tag}">{word}</a>{sub_navigator_html}</li></ul>'

        return navigator_html


def parse(text: str) -> str:
    """
    解析 markdown 文本转 html
    """
    assert type(text) == str, "输入应为字符串"

    # 空输入
    if not text.strip():
        return ""

    md = Markdown()
    return md.parse(text)


def parse_file(file_name: str) -> str:
    """
    解析 md 文件转 html
    """
    if not os.path.exists(file_name): # pragma: no cover
        print(f"fail to find {file_name}")
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()

    return parse(text)

def parse_toc(text: str) -> str:
    """
    解析 markdown 文本, 带目录树
    """
    assert type(text) == str, "输入应为字符串"

    # 空输入
    if not text.strip():
        return ""

    md = Markdown()
    return md.parse_with_tag(text)


def parse_file_toc(file_name: str) -> str:
    """
    解析 md 文件, 带目录树
    """
    with open(file_name, "r", encoding="utf-8") as f:
        text = f.read()

    return parse_toc(text)
