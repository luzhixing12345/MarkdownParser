
from .base_class import Parser,Handler,Block,_container,_counter
from typing import List
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

class ComplexBlock(Block):
    # 用于处理复杂嵌套
    
    def __init__(self, father:Block,**kwargs) -> None:
        super().__init__(**kwargs)
        self.father = father

class HTMLBlock(Block):
    # 处理HTML标签
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self):
        return '<html>'

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
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class HierarchyIndentHandler(Handler):
    # 匹配层次缩进
    # - 123
    #   hello world
    #   good luck
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'^([ ]{1,})(.*)')
        
    def __call__(self, root: Block, text: str):

        match_group = re.match(self.RE, text)
        space_number = len(match_group.group(1))
        word = match_group.group(2)
        
        block = HierarchyBlock(space_number=space_number)
        self.parser.match(block,word)
        root.addBlock(block)
        
        
class HierarchyBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class CodeBlockHandler(Handler):
    # 匹配代码段
    # ```python
    # a = 1
    # ```

    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'`{3,}(.*)')
        
    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        language = match_group.group(1).strip()
        return root.addBlock(CodeBlock(language=language))
        
class CodeBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class HashHeaderHandler(Handler):
    # 匹配标题
    # ### 123
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        
        # #开头,1-6个#均可 + 一个空格 + 文字
        self.RE = re.compile(r'(^#{1,6}) (.*)')
    
    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        level = len(match_group.group(1))
        header = match_group.group(2).strip() # 去掉头尾多余空格
        
        # 继续匹配header中的文字
        block = HashHeaderBlock(level=level,header=header)
        self.parser.match(block,header)
        root.addBlock(block)
        
class HashHeaderBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class TaskListHandler(Handler):
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'^[-+\*] \[([ x])\] (.*)')
        
    def __call__(self, root: Block, text: str):

        match_group = re.match(self.RE, text)
        is_complete = match_group.group(1)
        word = match_group.group(2)
        
        block = TaskListBlock(complete=is_complete,word=word)
        self.parser.match(block,word)
        root.addBlock(block)
        
class TaskListBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class OListHandler(Handler):
    # 匹配有序列表
    # 1. 123
    # 2. 123
    
    def __init__(self, parser:BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'^\d+\. (.*)')

    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        word = match_group.group(1)
        
        block = OListBlock(word=word)
        self.parser.match(block,word)
        root.addBlock(block)
        
class OListBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        

class UListHandler(Handler):
    
    def __init__(self, parser:BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'^[-+\*] (.*)')
        
    def __call__(self, root: Block, text: str):

        match_group = re.match(self.RE,text)
        word = match_group.group(1)
        
        block = UListBlock(word=word)
        self.parser.match(block,word)
        root.addBlock(block)

class UListBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
class QuoteHandler(Handler):
    # 匹配引用
    # > 123
    def __init__(self, parser:BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'^(>{1,}) (.*)')

    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        quote_number = len(match_group.group(1))
        word = match_group.group(2)
        block = QuoteBlock(quote_number=quote_number, word=word)
        self.parser.match(block,word)
        root.addBlock(block)
        
class QuoteBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class ParagraphHandler(Handler):
    # 匹配图片 
    # ![asd](123)
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        self.RE = re.compile(r'(?<!\\)!\[([^\!\[\]]*?)\]\((.*?)\)')
        
    def __call__(self, root: Block, text: str):
        
        match_groups = self.RE.finditer(text)     
        block = ComplexBlock(root)
        
        str_position = []                
        words = []
        urls = []
        for match_group in match_groups:
            start, end = match_group.span()
            word = match_group.group(1)
            url = match_group.group(2)
            
            str_position.append((start,end))
            words.append(word)
            urls.append(url)
        
        new_text = ''
        start_pos = 0
        for (word,url,(start,end)) in zip(words,urls,str_position):

            ref_block = ParagraphBlock(word=word,url=url)
            replace_name = block.register(ref_block) # 注册并替换名字
            new_text += text[start_pos:start] + replace_name
            start_pos = end
        new_text += text[start_pos:]
            
        self.parser.match(block,new_text)
        root.addBlock(block)

        
class ParagraphBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
        
class ReferenceHandler(Handler):
    # 处理引用
    # [1](abc)
    
    def __init__(self, parser:BlockParser) -> None:
        super().__init__()
        self.parser = parser
        # 匹配嵌套 + 忽略末尾多余 )
        self.RE = re.compile(r'(?<!\\)\[([^\[\]]*?)\]\((.*?)\)')  

    def __call__(self, root: Block, text: str):
        
        match_groups = self.RE.finditer(text)     
        block = ComplexBlock(root)
        
        str_position = []                
        words = []
        urls = []
        for match_group in match_groups:
            start, end = match_group.span()
            word = match_group.group(1)
            url = match_group.group(2)
            
            str_position.append((start,end))
            words.append(word)
            urls.append(url)
        
        new_text = ''
        start_pos = 0
        for (word,url,(start,end)) in zip(words,urls,str_position):

            ref_block = ReferenceBlock(word=word,url=url)
            replace_name = block.register(ref_block) # 注册并替换名字
            new_text += text[start_pos:start] + replace_name
            start_pos = end
        new_text += text[start_pos:]
            
        self.parser.match(block,new_text)
        root.addBlock(block)
        
class ReferenceBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)     


class SpecialTextHandler(Handler):
    # 处理特殊字符
    # 不考虑 * 的多级嵌套

    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        
        self.split_line = re.compile(r'^[-=\*]{3,} *$')      # 分隔符
        # <邮箱|网址>
        self.web_link = re.compile(r'(?<!\\)<(\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*|[a-zA-z]+:\/\/[^\s]*)>')
        # 粗体 + 斜体 ***1*** | **_1_**
        self.bold_italic = re.compile(r'(?<!\\)(?:\*{3}(.*+)\*{3}|\*{2}_(.*+)_\*{2})')
        self.italic = re.compile(r'(?<!\\)(?:_(.*+)_|\*(.*+)\*)')
        self.bold = re.compile(r'(?<!\\)\*{2}(.*+)\*{2}')
        self.delete = re.compile(r'(?<!\\)~~(.*+)~~')
        self.highlight = re.compile(r'(?<!\\)(?:`(.*+)`|``(.*+)``)')
        
        self.RE = [
            self.split_line, self.web_link, self.bold_italic,
            self.bold, self.delete,self.highlight
        ]
        
    def match(self, text: str, *args):

        for RE in self.RE:
            if bool(RE.search(text)):
                return True
        return False

    def __call__(self, root: Block, text: str):

        block = ComplexBlock(root)
        
        
        
class SpecialTextBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class TextHandler(Handler):
    # 处理常规文本
    
    def __init__(self, parser: BlockParser) -> None:
        super().__init__()
        self.parser = parser
        
    def match(self, text:str):  
        return True
    
    def __call__(self, root: Block, text: str):
        
        global _container
        RE = re.compile(r'({-%.*?%-})')
        split_strings = RE.split(text)

        count = 0
        for string in split_strings:
            # 正常文本字符
            if count % 2 == 0:
                if string:
                    root.addBlock(TextBlock(word=string))
            else:
                id = string[3:-3]
                class_object:Block = _container[id]
                class_object.restore(TextBlock)
                root.addBlock(class_object)
            count += 1
        
class TextBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


def buildBlockParser():

    block_parser = BlockParser()
    block_parser.register(EmptyBlockHandler(block_parser), 'empty', 100)
    block_parser.register(HierarchyIndentHandler(block_parser), 'indent', 90)
    block_parser.register(CodeBlockHandler(block_parser), 'code', 80)
    block_parser.register(HashHeaderHandler(block_parser), 'hashheader', 70)
    # block_parser.register(SetextHeaderHandler(), 'setextheader', 60)
    # block_parser.register(HRHandler(), 'hr', 50)
    block_parser.register(TaskListHandler(block_parser), 'tlist', 50)
    block_parser.register(OListHandler(block_parser), 'olist', 40)
    block_parser.register(UListHandler(block_parser), 'ulist', 30)
    block_parser.register(QuoteHandler(block_parser), 'quote', 20)
    block_parser.register(ParagraphHandler(block_parser), 'paragraph', 15)
    block_parser.register(ReferenceHandler(block_parser), 'reference', 10)
    # block_parser.register(SpecialTextHandler(block_parser), 'specialtext', 0)
    block_parser.register(TextHandler(block_parser), 'text', 0)
    return block_parser
