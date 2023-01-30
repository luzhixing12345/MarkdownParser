
import re
from .base_class import Parser, Optimizer, Block
from .block_parser import TableBlock, buildBlockParser, TextBlock


class TreeParser(Parser):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, root: Block):

        root.input['align_space_number'] = 0  # 用于 HierarchyEliminate 阶段的对齐空格调整

        self.checkBlock(root)
        return root

    def checkBlock(self, block: Block):
        # 深度优先的遍历root的所有节点,
        # 如果遇到相应的可优化项则将节点交由对应的优化器处理
        for optimizer in self._handlers:
            optimizer['object'](block)

        if block.sub_blocks == []:
            return
        else:
            for sub_block in block.sub_blocks:
                self.checkBlock(sub_block)


class HierarchyMerge(Optimizer):
    # 合并相同层级(space_number)

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['HierarchyBlock', 'EmptyBlock']

    def __call__(self, root: Block):

        new_sub_blocks = []
        activite_block = None
        activite_space_number = 0

        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                # EmptyBlock的处理相当于任意的space_number的HierarchyBlock
                # space_number = -1

                # first meet
                if activite_block is None:
                    activite_space_number = block.input.get('space_number', -1)
                    # 未在匹配状态的EmptyBlock不算入
                    if activite_space_number == -1:
                        new_sub_blocks.append(block)
                    else:
                        activite_block = block
                else:
                    current_space_number = block.input.get('space_number', -1)

                    # 不处理连续的EmptyBlock
                    if current_space_number == -1:
                        if activite_block.sub_blocks[-1].block_name == 'EmptyBlock':
                            continue
                        else:
                            activite_block.sub_blocks.append(block)
                    # 层次相同,合并
                    elif current_space_number == activite_space_number:
                        activite_block.input['text'] += '\n' + \
                            block.input['text']
                        activite_block.sub_blocks.extend(block.sub_blocks)
                    else:
                        # 层次缩进改变
                        new_sub_blocks.append(activite_block)
                        activite_block = block
                        activite_space_number = current_space_number
            else:
                if activite_block is not None:
                    new_sub_blocks.append(activite_block)
                    activite_block = None
                new_sub_blocks.append(block)

        if activite_block is not None:
            new_sub_blocks.append(activite_block)

        root.sub_blocks = new_sub_blocks


class QuoteBlockMerge(Optimizer):
    # 合并相同层级的引用模块
    # 与HierarchyBlock不同的是,引用模块中EmptyBlock作为区分符

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['QuoteBlock']

    def __call__(self, root: Block):

        new_sub_blocks = []
        activite_block = None

        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                if activite_block is None:
                    activite_block = block
                else:
                    activite_block.sub_blocks.extend(block.sub_blocks)
            else:
                if activite_block is not None:
                    new_sub_blocks.append(activite_block)
                    activite_block = None
                new_sub_blocks.append(block)

        if activite_block is not None:
            new_sub_blocks.append(activite_block)

        root.sub_blocks = new_sub_blocks


class CodeBlockOptimizer(Optimizer):
    # 将代码段之间的代码恢复为纯文本并保存在input['code']

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['CodeBlock']

    def __call__(self, root: Block):

        activite_CodeBlock = None
        restore_text = False
        new_sub_blocks = []

        for i in range(len(root.sub_blocks)):

            block: Block = root.sub_blocks[i]
            # 开始恢复纯文本
            if restore_text:
                # 再一次遇到代码段标志,意味着结束
                if block.block_name in self.target_block_names:
                    restore_text = False
                    # 去掉结尾换行符
                    activite_CodeBlock.input['code'] = activite_CodeBlock.input['code'][:-1]
                    new_sub_blocks.append(activite_CodeBlock)
                    activite_CodeBlock = None
                    continue
                activite_CodeBlock.input['code'] += block.input['text'] + '\n'
            else:
                if block.block_name in self.target_block_names:
                    restore_text = True
                    activite_CodeBlock = block
                else:
                    new_sub_blocks.append(block)

        # 代码段不匹配,一直到结尾全部恢复为文本
        if activite_CodeBlock is not None:
            # 去掉结尾换行符
            activite_CodeBlock.input['code'] = activite_CodeBlock.input['code'][:-1]
            new_sub_blocks.append(activite_CodeBlock)

        root.sub_blocks = new_sub_blocks


class HierarchyEliminate(Optimizer):
    # 消除多余EmptyBlock
    # 消除Hierarchy标签,调整UList OList对齐关系

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['UListBlock', 'OListBlock']

        self.interrupt_block_names = [
            'CodeBlock', 'HashHeaderBlock', 'TableBlock', 'QuoteBlock', 'SplitBlock']
        # 递进级层次缩进被打断
        # 例子:
        #
        # - 123
        # # abc
        #   - aaa

    def __call__(self, root: Block):

        # 当前节点的所需的对齐空格长度
        # 如果没有该属性则说明不需要考虑层次缩进的情况
        root_align_space_number = root.input.get('align_space_number', None)
        if root_align_space_number is None:
            return

        new_sub_blocks = []
        activite_block = None
        deeper_indent = False

        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                # 对齐长度从根节点依次传递下去
                block.input['align_space_number'] += root_align_space_number
                # 切换
                if deeper_indent:
                    new_sub_blocks.append(activite_block)
                deeper_indent = True
                activite_block = block
            elif block.block_name in self.interrupt_block_names:
                deeper_indent = False
                if activite_block is not None:
                    new_sub_blocks.append(activite_block)
                    activite_block = None
                new_sub_blocks.append(block)

            elif block.block_name == 'HierarchyBlock':
                if deeper_indent:
                    left_space_number = block.input['space_number'] - \
                        activite_block.input['align_space_number']
                    # 刚好满足缩进,直接展开
                    if left_space_number == 0:
                        activite_block.sub_blocks.extend(block.sub_blocks)
                    # 空格数多余缩进所需,归入activite_block节点放到下层处理
                    elif left_space_number > 0:
                        activite_block.addBlock(block)
                    # 空格数少于缩进所需, 归并到根节点
                    else:
                        if activite_block is not None:
                            new_sub_blocks.append(activite_block)
                            activite_block = None
                            deeper_indent = False
                        new_sub_blocks.extend(block.sub_blocks)
                # 递进级层次缩进被打断
                else:
                    new_sub_blocks.extend(block.sub_blocks)
            else:
                # EmptyBlock 先补齐在 UList OListBlock 下
                if block.block_name == 'EmptyBlock':
                    if deeper_indent:
                        if len(activite_block.sub_blocks) == 0:
                            activite_block.addBlock(block)
                        # 忽略连续的EmptyBlock
                        elif activite_block.sub_blocks[-1].block_name != 'EmptyBlock':
                            activite_block.addBlock(block)
                    else:
                        if len(new_sub_blocks) > 1 and new_sub_blocks[-1].block_name == 'EmptyBlock':
                            continue
                        else:
                            new_sub_blocks.append(block)
                else:
                    if activite_block is not None:
                        new_sub_blocks.append(activite_block)
                        activite_block = None
                        deeper_indent = False
                    new_sub_blocks.append(block)

        if activite_block is not None:
            new_sub_blocks.append(activite_block)

        root.sub_blocks = new_sub_blocks


class OListSerialOptimizer(Optimizer):
    # 优化 Olist 序号顺序

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['OListBlock', 'EmptyBlock']

    def __call__(self, root: Block):

        new_sub_blocks = []
        first_number = None

        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                if block.block_name == 'EmptyBlock':
                    continue
                if first_number is None:
                    first_number = int(block.input['serial_number'])
                else:
                    first_number += 1
                    block.input['serial_number'] = str(first_number)
            else:
                first_number = None
                new_sub_blocks.append(block)


class ExtensionOptimizer(Optimizer):

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['ExtensionBlock']
        self.extension_tag = ['note', 'info', 'success']

    def __call__(self, root: Block):

        activite_block = None
        new_sub_blocks = []

        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                if block.input['tag'] in self.extension_tag:
                    if activite_block is None:
                        activite_block = block
                    # 不支持嵌套使用, 恢复为纯文本
                    else:
                        activite_block.addBlock(
                            TextBlock(text=block.input['text'], word=block.input['text']))
                elif block.input['tag'] == 'end':
                    if activite_block is None:
                        new_sub_blocks.append(
                            TextBlock(text=block.input['text'], word=block.input['text']))
                    else:
                        new_sub_blocks.append(activite_block)
                        activite_block = None
                else:
                    raise KeyError("Unknown tag " + block.input['tag'])
            else:
                if activite_block is not None:
                    activite_block.addBlock(block)
                else:
                    new_sub_blocks.append(block)

        if activite_block is not None:
            new_sub_blocks.append(activite_block)

        root.sub_blocks = new_sub_blocks


class TableBlockOptimizer(Optimizer):

    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r'(?<!\\)\|')
        self.block_parser = buildBlockParser()  # 初始化一个block parser 用于解析表格中出现的每一个表项
        # 匹配的
        self.table_block_names = ['TableBlock']

        # 表格匹配,其余中断
        self.header_block_names = ['TextBlock', 'ComplexBlock']
        self.body_block_names = ['TextBlock', 'ComplexBlock', 'TableBlock']

    def _createTableBlock(self, header_block: Block, table_block: Block):
        # 判断header和table列是否匹配
        # 匹配返回一个TableBlock对象实例,用于后续补充表格
        # 不匹配返回None
        table_length = len(table_block.input['alignments'])
        header_text = header_block.input['text']  # 获取原文

        header = self.RE.split(header_text)
        if len(header)-2 != table_length:
            return None

        # 匹配,创建实例
        header = header[1:-1]
        for i in range(len(header)):
            header[i] = header[i].strip()
        # 重新解析每一个table的表项
        table_header_node = self.block_parser(header)

        header_info = [i.input['word'] for i in table_header_node.sub_blocks]
        table_header_node.input['ifno'] = header_info
        new_table_block = TableBlock(
            header=table_header_node,
            alignments=table_block.input['alignments'],
            length=len(header)
        )
        return new_table_block

    def _addTableItem(self, table_block: TableBlock, table_item_block: Block):
        # 添加表格项,多去少补
        table_items = self.RE.split(table_item_block.input['text'])
        if not table_items[0]:
            table_items.pop(0)
        if not table_items[-1]:
            table_items.pop()
        table_length = table_block.input['length']
        if len(table_items) > table_length:
            table_items = table_items[:table_length]
        else:
            table_items.extend(
                [' ' for _ in range(table_length-len(table_items))])
        for i in range(len(table_items)):
            table_items[i] = table_items[i].strip()

        table_item_node = self.block_parser(table_items)
        for i in range(len(table_item_node.sub_blocks)):
            if table_item_node.sub_blocks[i].__class__.__name__ == 'EmptyBlock':
                table_item_node.sub_blocks[i] = TextBlock(text='', word='')
        table_block._addTableItem(table_item_node)
        # table_item_node.info()

    def __call__(self, root: Block):

        new_sub_blocks = []
        table_block = None
        # 分两步匹配
        # 1. header + table 的BlockName匹配
        # 2. header 和 table 的列个数匹配
        match_table = False
        # root.info()
        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            # 进入匹配阶段
            if match_table:
                # 中断匹配
                if block.block_name not in self.body_block_names:
                    match_table = False
                    new_sub_blocks.append(table_block)
                    table_block = None
                else:
                    self._addTableItem(table_block, block)
                    continue
            # 尝试匹配 TableBlock, 开头不可以
            if block.block_name in self.table_block_names and i != 0:
                # 第一步匹配
                if root.sub_blocks[i-1].block_name in self.header_block_names:
                    # 第二步匹配
                    table_block = self._createTableBlock(
                        root.sub_blocks[i-1], block)
                    # 匹配成
                    if table_block is not None:
                        match_table = True
                        # 把上一项header的TextBlock那一项退出来,已经整合到table_block中了
                        new_sub_blocks.pop()
                    else:
                        # 将TableBlock变为纯文本
                        new_sub_blocks.append(
                            TextBlock(text=block.input['text'], word=block.input['text']))
                        match_table = False
                else:
                    new_sub_blocks.append(block)
            else:
                new_sub_blocks.append(block)

        if table_block is not None:
            new_sub_blocks.append(table_block)
        root.sub_blocks = new_sub_blocks


class ParagraphOptimizer(Optimizer):
    # 将元素使用 ParagraphBlock 包裹起来
    # 以便创建p标签换行

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['TextBlock', 'ComplexBlock', 'ReferenceBlock',
                                   'PictureBlock', 'SpecialTextBlock', 'EscapeCharacterBlock']
        self.interrupt_block_names = ['ParagraphBlock', 'HashHeaderBlock', 'EscapeCharacterBlock',
                                      'TableBlock', 'HTMLBlock', 'QuoteBlock',
                                      'ComplexBlock', 'ReferenceBlock', 'PictureBlock',
                                      'SpecialTextBlock', 'AnnotateBlock']

    def __call__(self, root: Block):

        if root.__class__.__name__ in self.interrupt_block_names:
            return
        activite_block = None
        new_sub_blocks = []

        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                # 特殊情况,不划入ParagraphBlock
                if root.__class__.__name__ in ['OListBlock', 'UListBlock'] and i == 0:
                    new_sub_blocks.append(block)
                elif activite_block is None:
                    activite_block = ParagraphBlock()
                    activite_block.addBlock(block)
                else:
                    activite_block.addBlock(block)
            else:
                if activite_block is not None:
                    new_sub_blocks.append(activite_block)
                    activite_block = None
                new_sub_blocks.append(block)

        if activite_block is not None:
            new_sub_blocks.append(activite_block)

        root.sub_blocks = new_sub_blocks


class ParagraphBlock(Block):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def toHTML(self):

        content = ''
        for block in self.sub_blocks:
            content += block.toHTML()
        return f'<p>{content}</p>'


class SpecialTextOptimizer(Optimizer):
    # 将高亮的文本恢复回
    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['SpecialTextBlock']

    def __call__(self, root: Block):
        # return
        if root.__class__.__name__ in self.target_block_names and root.input['tag'] == 'highlight':
            for i in range(len(root.sub_blocks)):
                block: Block = root.sub_blocks[i]
                origin_text = block.input['text']
                # 替换以消除html元素影响
                origin_text = re.sub('<', '&lt;', origin_text)
                origin_text = re.sub('>', '&gt;', origin_text)
                root.sub_blocks[i] = TextBlock(
                    text=origin_text, word=origin_text)


def buildTreeParser():
    # tree parser 用于优化并得到正确的解析树
    tree_parser = TreeParser()
    tree_parser.register(HierarchyMerge(), 100)
    tree_parser.register(QuoteBlockMerge(), 95)
    tree_parser.register(CodeBlockOptimizer(), 90)
    tree_parser.register(HierarchyEliminate(), 85)
    tree_parser.register(OListSerialOptimizer(), 80)
    # tree_parser.register(ExtensionOptimizer(),70)
    tree_parser.register(TableBlockOptimizer(), 60)
    tree_parser.register(ParagraphOptimizer(), 50)
    tree_parser.register(SpecialTextOptimizer(), 0)
    return tree_parser
