
from .base_class import Parser,Handler,Block
from typing import List,Union
import re



class BlockParser(Parser):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, lines: List[str]):

        self.root = Block()
        self._sort()

        for text in lines:
            self.match(self.root, text)
                    
        self.root.info()
        
    def match(self, root:Block, text:str):

        for method in self._handlers:
            if method['object'].match(text):
                # print('[',text,']',method['name'] + ' matched')
                method['object'](root, text)
                return
            else:
                # print(method['name'] + ' missed')
                pass

class EmptyBlockHandler(Handler):
    # 处理空行
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser

    def match(self, text: str):
        return not text.strip()

    def __call__(self, root: Block, text: str):
        root.addBlock(EmptyBlock())
    
class EmptyBlock(Block):
    
    def __init__(self) -> None:
        super().__init__()
    
class HashHeaderHandler(Handler):
    # 匹配标题
    # ### 123
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        
        # #开头,1-6个#均可 + 一个空格 + 文字
        self.RE = re.compile(r'(^#{1,6}) (.*)')
        
    def match(self, text: str):
        return bool(self.RE.search(text))
    
    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        level = len(match_group.group(1))
        header = match_group.group(2)
        
        # 继续匹配header中的文字
        block = HashHeaderBlock(level,header)
        self.parser.match(block,header)
        root.addBlock(block)
        
class HashHeaderBlock(Block):
    
    def __init__(self, level: int, header: str or Block=None) -> None:
        super().__init__()
        self.level = level
        self.header = header
        
    def __str__(self):
        return f'<level = {self.level}, header = {self.header}>'


class ReferenceHandler(Handler):
    
    def __init__(self, parser:BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'\[(.*?)\]\((.*?)\)')  
    
    def match(self, text: str):
        
        return bool(self.RE.search(text))

    def __call__(self, root: Block, text: str):
        
        match_groups = self.RE.finditer(text)     
        block = Block()
        
        # 剩余字符匹配的起始位置
        rest_position = 0
        
        for match_group in match_groups:
            start, end = match_group.span()
            word = match_group.group(1)
            url = match_group.group(2)
            print(start,end,word,url)
            rest_str = text[rest_position:start]
            if rest_str:
                self.parser.match(block,rest_str)
            rest_position = end
            ref_block = ReferenceBlock(word,url)
            block.addBlock(ref_block)
        
        # 匹配结尾的文字
        rest_str = text[rest_position:]
        if rest_str.rstrip():
            self.parser.match(block,rest_str)
        
        if len(block.sub_blocks) == 1:
            block = block.sub_blocks[0]
                
        root.addBlock(block)
        
class ReferenceBlock(Block):
    
    def __init__(self, word: str=None, url: str=None) -> None:
        super().__init__()
        self.word = word
        self.url = url

    def __str__(self):
        return f'<word = {self.word}, url = {self.url}>'        

class ParagraphHandler(Handler):
    # 匹配图片 
    # ![asd](123)
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'!\[(.*?)\]\((.*?)\)')
        
    def match(self, text: str):
        
        return bool(self.RE.search(text))
    
    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE, text)
        word = match_group.group(1) # 文字部分
        url = match_group.group(2)  # 链接部分
        
        root.addBlock(ParagraphBlock(word, url))

        
class ParagraphBlock(Block):
    
    def __init__(self, word: str, url: str) -> None:
        super().__init__()
        self.word = word
        self.url = url        
    
    def __str__(self):
        return f'<word = {self.word}, url = {self.url}>'

class TextHandler(Handler):
    # 处理常规文本
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        
    def match(self, text:str):
        return True
    
    def __call__(self, root: Block, text: str):
        
        root.addBlock(TextBlock(text))
        
class TextBlock(Block):
    
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def __str__(self):
        return f'<text = {self.text}>'


def buildBlockParser():

    block_parser = BlockParser()
    block_parser.register(EmptyBlockHandler(block_parser), 'empty', 100)
    # block_parser.register(ListIndentHandler(), 'indent', 90)
    # block_parser.register(CodeBlockHandler(), 'code', 80)
    block_parser.register(HashHeaderHandler(block_parser), 'hashheader', 70)
    # block_parser.register(SetextHeaderHandler(), 'setextheader', 60)
    # block_parser.register(HRHandler(), 'hr', 50)
    # block_parser.register(OListHandler(), 'olist', 40)
    # block_parser.register(UListHandler(), 'ulist', 30)
    # block_parser.register(BlockQuoteHandler(), 'quote', 20)
    block_parser.register(ReferenceHandler(block_parser), 'reference', 15)
    block_parser.register(ParagraphHandler(block_parser), 'paragraph', 10)
    block_parser.register(TextHandler(block_parser), 'text', 0)
    return block_parser
