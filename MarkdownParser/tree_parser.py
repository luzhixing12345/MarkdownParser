

from .base_class import Parser, Optimizer, Block
from .block_parser import ParaphgraphBlock,TextBlock, CodeBlock,OListBlock,UListBlock

class TreeParser(Parser):
    
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, root:Block):

        self.checkBlock(root)
        root.info()
        ...

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



class CodeBlockOptimizer(Optimizer):
    # 将代码段start-end之间的代码恢复为纯文本并保存在input['code']

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['CodeBlock']
        
    def __call__(self, root: Block):
        
        current_CodeBlock:CodeBlock = None
        restore_text = False
        new_sub_blocks = []
        
        for i in range(len(root.sub_blocks)):
            
            block : Block = root.sub_blocks[i]
            # 开始恢复纯文本
            if restore_text:
                if block.block_name in self.target_block_names:
                    if block.input['type'] == 'end':
                        restore_text = False
                        current_CodeBlock.input['code'] = current_CodeBlock.input['code'][:-1] # 去掉结尾换行符
                        current_CodeBlock.input['type'] = 'full' # 完整的代码段
                        new_sub_blocks.append(current_CodeBlock)
                        current_CodeBlock = None
                        continue
                # print(block.__class__.__name__,'!')
                current_CodeBlock.input['code'] += block.input['text'] + '\n'
                self.is_match = True
            else:
                if block.block_name in self.target_block_names:
                    if block.input['type'] == 'start':
                        restore_text = True
                        current_CodeBlock = block
                else:
                    new_sub_blocks.append(block)
        
        # 代码段不匹配,一直到结尾全部恢复为文本
        if current_CodeBlock:
            current_CodeBlock.input['code'] = current_CodeBlock.input['code'][:-1] # 去掉结尾换行符
            current_CodeBlock.input['type'] = 'full' # 完整的代码段
            new_sub_blocks.append(current_CodeBlock)
                          
        root.sub_blocks = new_sub_blocks
        return self.is_match
            

class OUListOptimizer(Optimizer):
    
    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['OListBlock','UListBlock']
        
    def __call__(self, root: Block):

        ...

class ParagraphBlockOptimizer(Optimizer):
    
    # [TextBlock] < word = "虽然它们写在两行" >
    # [TextBlock] < word = "但是它们应该在一行" >
    #
    # [TextBlock] < word = "虽然它们写在两行 但是它们应该在一行" >

    def __init__(self) -> None:
        super().__init__()
        self.target_block_names = ['TextBlock','ReferenceBlock','SpecialBlock','PictureBlock','ComplexBlock']
    
    def __call__(self, root: Block):
                
        # 1. 合并连续的TextBlock
        # 2. 删除多行空行
        # 3. 展开ComplexBlock
        # block = ParaphgraphBlock()
        meet = False # 是否遇到TextBlock
        current_TextBlock = None # 第一个TextBlock
        new_sub_blocks = []
        
        for i in range(len(root.sub_blocks)):
            block : Block = root.sub_blocks[i]
            if block.block_name in self.target_block_names:
                if meet:
                    # 再次遇到
                    self.is_match = True
                    current_TextBlock.input['word'] += ' ' + block.input['word']
                    # print(first_TextBlock._word)
                else:
                    # 第一次遇到
                    meet = True
                    current_TextBlock = block
            else:
                if meet:
                    new_sub_blocks.append(current_TextBlock)
                new_sub_blocks.append(block)
                meet = False
                current_TextBlock = None
        # 处理一下最后一个
        if meet:
            new_sub_blocks.append(current_TextBlock)
                
        root.sub_blocks = new_sub_blocks

        return self.is_match




def buildTreeParser():
    # tree parser 用于优化并得到正确的解析树
    tree_parser = TreeParser()
    tree_parser.register(CodeBlockOptimizer(),'code block optimize',100)
    # tree_parser.register(OUListOptimizer(),'O list and U list optimize',90)
    # tree_parser.register(ParagraphBlockOptimizer(),'paragraph optimize')
    return tree_parser