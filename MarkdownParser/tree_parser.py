
import re
from .base_class import Parser, Optimizer, Block
from .block_parser import TableBlock, buildBlockParser, TextBlock

class TreeParser(Parser):
    
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, root:Block):

        self.checkBlock(root)
        print(root.printInfo())

    def checkBlock(self, block:Block):
        # 深度优先的遍历root的所有节点,
        # 如果遇到相应的可优化项则将节点交由对应的优化器处理
        for optimizer in self._handlers:
            if optimizer['object'](block):
                break
            
        if block.sub_blocks == []:
            return
        else:
            for sub_block in block.sub_blocks:
                self.checkBlock(sub_block)

class HierarchyIndentOptimizer(Optimizer):
    # 合并相同层级
    
    def __init__(self) -> None:
        super().__init__()
        # EmptyBlock的处理相当于任意的space_number的HierarchyBlock
        self.target_block_names = ['HierarchyBlock','EmptyBlock']
        
    def __call__(self, root: Block):

        new_sub_blocks = []
        activite_block = None
        activite_space_number = 0
        
        for i in range(len(root.sub_blocks)):
            block:Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                # EmptyBlock的处理相当于任意的space_number的HierarchyBlock
                # space_number = -1
                
                # first meet
                if activite_block is None:
                    activite_block = block
                    activite_space_number = block.input.get('space_number',-1)
                else:
                    current_space_number = block.input.get('space_number',-1)                       
                    if activite_space_number == -1:
                        # 多个连续EmptyBlock, 不处理后续的EmptyBlock
                        if current_space_number == -1:
                            continue
                        else:
                            # 修正为遇到的第一个HierarchyBlock的space_number
                            activite_space_number = current_space_number
                            activite_block = block
                        
                    else:
                        # 多个连续EmptyBlock, 不处理后续的EmptyBlock
                        if current_space_number == -1 and activite_block.sub_blocks[-1].block_name == 'EmptyBlock':
                            continue
                        if current_space_number == activite_space_number or current_space_number == -1:
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
        return self.is_match


class CodeBlockOptimizer(Optimizer):
    # 将代码段start-end之间的代码恢复为纯文本并保存在input['code']

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['CodeBlock']
        
    def __call__(self, root: Block):
        
        activite_CodeBlock = None
        restore_text = False
        new_sub_blocks = []
        
        for i in range(len(root.sub_blocks)):
            
            block : Block = root.sub_blocks[i]
            # 开始恢复纯文本
            if restore_text:
                # 再一次遇到代码段标志,意味着结束
                if block.block_name in self.target_block_names:
                    restore_text = False
                    activite_CodeBlock.input['code'] = activite_CodeBlock.input['code'][:-1] # 去掉结尾换行符
                    new_sub_blocks.append(activite_CodeBlock)
                    activite_CodeBlock = None
                    continue
                activite_CodeBlock.input['code'] += block.input['text'] + '\n'
                self.is_match = True
            else:
                if block.block_name in self.target_block_names:
                    restore_text = True
                    activite_CodeBlock = block
                else:
                    new_sub_blocks.append(block)
        
        # 代码段不匹配,一直到结尾全部恢复为文本
        if activite_CodeBlock is not None:
            activite_CodeBlock.input['code'] = activite_CodeBlock.input['code'][:-1] # 去掉结尾换行符
            new_sub_blocks.append(activite_CodeBlock)
                          
        root.sub_blocks = new_sub_blocks
        return self.is_match
            
class HashHeaderBlockOptimizer(Optimizer):
    
    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['HashHeaderBlock']
        
    def __call__(self, root: Block):

        for block in root.sub_blocks:
            if block.block_name in self.target_block_names:
                # HashBlock 有且仅有一个sub, sub_blocks[0]
                # 如果是复杂文本则将ComplexBlock.sub_blocks传递给HashBlock
                # 目的是剔除HashBlock中的ComplexBlock影响
                # 以便后续使用ParagraphBlock处理所有剩余的ComplexBlock
                if block.sub_blocks[0].block_name == 'ComplexBlock':
                    block.sub_blocks = block.sub_blocks[0].sub_blocks
                    self.is_match = True
        
        return self.is_match

class TableBlockOptimizer(Optimizer):
    
    def __init__(self) -> None:
        super().__init__()
        self.RE = re.compile(r'(?<!\\)\|')
        self.block_parser = buildBlockParser() # 初始化一个block parser 用于解析表格中出现的每一个表项
        # 匹配的
        self.table_block_names = ['TableBlock']
        
        # 表格匹配,其余中断
        self.header_block_names = ['TextBlock','ComplexBlock']
        self.body_block_names = ['TextBlock','ComplexBlock','TableBlock']
        
    def _matchSize(self,header_block:Block, table_block:Block):
        # 判断header和table列是否匹配
        # 匹配返回一个TableBlock对象实例,用于后续补充表格
        # 不匹配返回None
        table_length = len(table_block.input['alignments'])
        header_text = header_block.input['text'] # 获取原文
        
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

    def _addTableItem(self,table_block: TableBlock, table_item_block:Block):
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
            table_items.extend([' ' for _ in range(table_length-len(table_items))])
        for i in range(len(table_items)):
            table_items[i] = table_items[i].strip()
        
        table_item_node = self.block_parser(table_items)
        for i in range(len(table_item_node.sub_blocks)):
            if table_item_node.sub_blocks[i].__class__.__name__ == 'EmptyBlock':
                table_item_node.sub_blocks[i] = TextBlock(text=' ',word='')
        table_block._addTableItem(table_item_node)
        # table_item_node.info()
        
    def __call__(self, root: Block):

        new_sub_blocks = []
        table_block = None
        # 分两步匹配
        # 1. header + table 的BlockName匹配
        # 2. header 和 table 的列个数匹配
        match_table = False

        for i in range(len(root.sub_blocks)):
            block:Block = root.sub_blocks[i]
            # 进入匹配阶段
            if match_table:
                # 中断匹配
                if block.block_name not in self.body_block_names:
                    match_table = False
                    new_sub_blocks.append(table_block)
                    table_block = None
                else:
                    self._addTableItem(table_block,block)
                    continue
            # 尝试匹配 TableBlock, 开头不可以
            if block.block_name in self.table_block_names and i!=0:
                # 第一步匹配
                if root.sub_blocks[i-1].block_name in self.header_block_names:
                    # 第二步匹配
                    table_block = self._matchSize(root.sub_blocks[i-1],block)
                    if table_block is not None:
                        match_table = True
                        # 把上一项header的TextBlock那一项退出来,已经整合到table_block中了
                        new_sub_blocks.pop()
                        self.is_match = True
                        continue
                    else:
                        match_table = False

            # 几个else情况
            new_sub_blocks.append(block)
        
        if table_block is not None:
            new_sub_blocks.append(table_block)
        root.sub_blocks = new_sub_blocks
        return self.is_match

class UListOptimizer(Optimizer):
    # 将连续的 Olist / Ulist 合并起来
    
    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['EmptyBlock','UListBlock']
        
    def __call__(self, root: Block):

        new_sub_blocks = []
        activite_block = None
        
        for i in range(len(root.sub_blocks)):
            block: Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                if activite_block is None:
                    activite_block = block
                else:
                    activite_block.sub_blocks.append(block)
            else:
                new_sub_blocks.append(block)

class ParagraphBlockOptimizer(Optimizer):
    
    # 1. 合并连续的TextBlock
    # 2. 删除多行空行
    # 3. 将上述 Blocks 整合到 ParagraphBlock中    

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['TextBlock','ReferenceBlock','SpecialBlock','PictureBlock','ComplexBlock']
    
    def __call__(self, root: Block):
                
        paraphgraph_block = None
        new_sub_blocks = []
        
        for i in range(len(root.sub_blocks)):
            block : Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                if paraphgraph_block:
                    # 再次遇到
                    activite_Block.input['word'] += ' ' + block.input['word']
                    # print(first_TextBlock._word)
                else:
                    # 第一次遇到
                    meet = True
                    activite_Block = block
            else:
                if meet:
                    new_sub_blocks.append(activite_Block)
                new_sub_blocks.append(block)
                meet = False
                activite_Block = None
        # 处理一下最后一个
        if meet:
            new_sub_blocks.append(activite_Block)
                
        root.sub_blocks = new_sub_blocks

        return self.is_match




def buildTreeParser():
    # tree parser 用于优化并得到正确的解析树
    tree_parser = TreeParser()
    tree_parser.register(HierarchyIndentOptimizer(),100)
    tree_parser.register(CodeBlockOptimizer(),90)
    tree_parser.register(HashHeaderBlockOptimizer(),80)
    tree_parser.register(TableBlockOptimizer(),70)
    # tree_parser.register(UListOptimizer(),60)
    # tree_parser.register(ParagraphBlockOptimizer(),'paragraph optimize',80)
    return tree_parser