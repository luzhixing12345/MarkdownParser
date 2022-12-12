
from .base_class import Parser,Handler,Block,CONTAINER
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
        # self.root.info()
        return self.root
        
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
    
    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)

class HTMLBlock(Block):
    # 处理HTML标签
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __str__(self):
        return '<html>'
    
class ParaphgraphBlock(Block):
    # 在本阶段不使用,在优化阶段使用
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class EmptyBlockHandler(Handler):
    # 处理空行
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        
    def match(self, text: str):
        return not text.strip()

    def __call__(self, root: Block, text: str):
        root.addBlock(EmptyBlock(text=text))
    
class EmptyBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class EscapeCharacterHandler(Handler):
    # 处理所有转义字符\以及其后面的一个字符
    
    def __init__(self, parser=None) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'\\(.)')

    def subFunc(self,match:re.Match):
        character = match.group(1)
        pic_block = EscapeCharacterBlock(word=character)
        replace_name = self.block.register(pic_block) # 注册并替换名字
        return replace_name
        
    def __call__(self, root: Block, text: str):
        
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text       
        new_text = re.sub(self.RE,self.subFunc,text)
        
        self.parser.match(self.block,new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block.sub_blocks[0].input['text'] = text
            self.block = self.block.sub_blocks[0]
            
        root.addBlock(self.block)

class EscapeCharacterBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class ExtensionBlockHandler(Handler):
    # 自定义扩展
    # {% note %}
    # asdklja
    # {%end%}
    
    def __init__(self, parser=None) -> None:
        super().__init__(parser)
        self.RE = re.compile(r"""(
            (^{[ ]*%[ ]*note[ ]*%[ ]*}[ ]*)|
            (^{[ ]*%[ ]*info[ ]*%[ ]*}[ ]*)|
            (^{[ ]*%[ ]*success[ ]*%[ ]*}[ ]*)|
            (^{[ ]*%[ ]*end[ ]*%[]*}[ ]*)
        )""",re.VERBOSE)
        
        self.groupid_tag = {
            2: 'note',
            3: 'info',
            4: 'success',
            5: 'end'
        }
        
    def __call__(self, root: Block, text: str):
        match = re.match(self.RE,text)
        # print(match)
        for k,v in self.groupid_tag.items():
            if match.group(k):
                tag = v
                break
        self.block = ExtensionBlock(text=text,tag=tag)
        root.addBlock(self.block)
        

class ExtensionBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class SplitBlockHandler(Handler):
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'^[-=\*]{3,} *$')      # 分隔符
    
    def __call__(self, root: Block, text: str):
        root.addBlock(SplitBlock(text=text))
        
class SplitBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def __str__(self):
        return '---<br>---'

class HierarchyIndentHandler(Handler):
    # 匹配层次缩进
    # - 123
    #   hello world
    #   good luck
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'^([ ]{1,})(.*)')
        
    def __call__(self, root: Block, text: str):

        match_group = re.match(self.RE, text)
        space_number = len(match_group.group(1))
        word = match_group.group(2)
        
        block = HierarchyBlock(space_number=space_number,text=text)
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

    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'`{3,}(.*)')
        
    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        language = match_group.group(1).strip()
        if language:
            # 代码段开头
            root.addBlock(CodeBlock(language=language,text=text,type='start'))
        else:
            # 代码段结尾
            root.addBlock(CodeBlock(text=text,type='end'))
        
class CodeBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        # code用于在优化阶段用于整合所有的代码
        super().__init__(code='',**kwargs)
        
class HashHeaderHandler(Handler):
    # 匹配标题
    # ### 123
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.parser = parser
        
        # #开头,1-6个#均可 + 一个空格 + 文字
        # Typora               r'(^#{1,6}) (.+)'
        # Markdown All in One  r'(^#{1,6}) (.?)'
        self.RE = re.compile(r'(^#{1,6}) (.+)')
    
    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        level = len(match_group.group(1))
        header = match_group.group(2).strip() # 去掉头尾多余空格
        
        # 继续匹配header中的文字
        block = HashHeaderBlock(level=level,header=header,text=text)
        self.parser.match(block,header)
        root.addBlock(block)
        
class HashHeaderBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class TaskListHandler(Handler):
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'^[-+\*] \[([ x])\] (.*)')
        
    def __call__(self, root: Block, text: str):

        match_group = re.match(self.RE, text)
        is_complete = match_group.group(1)
        word = match_group.group(2)
        
        block = TaskListBlock(complete=is_complete,word=word,text=text)
        self.parser.match(block,word)
        root.addBlock(block)
        
class TaskListBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class OListHandler(Handler):
    # 匹配有序列表
    # 1. 123
    # 2. 123
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'^\d+\. (.*)')

    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        word = match_group.group(1)
        
        block = OListBlock(word=word,text=text)
        self.parser.match(block,word)
        root.addBlock(block)
        
class OListBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        

class UListHandler(Handler):
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'^[-+\*] (.*)')
        
    def __call__(self, root: Block, text: str):

        match_group = re.match(self.RE,text)
        word = match_group.group(1)
        
        block = UListBlock(word=word,text=text)
        self.parser.match(block,word)
        root.addBlock(block)

class UListBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
class QuoteHandler(Handler):
    # 匹配引用
    # > 123
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'^(>{1,}) (.*)')

    def __call__(self, root: Block, text: str):
        
        match_group = re.match(self.RE,text)
        quote_number = len(match_group.group(1))
        word = match_group.group(2)
        block = QuoteBlock(quote_number=quote_number, word=word, text=text)
        self.parser.match(block,word)
        root.addBlock(block)
        
class QuoteBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class PictureHandler(Handler):
    # 匹配图片 
    # ![asd](123)
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'!\[([^\!\[\]]*?)\]\((.*?)\)')
        
    def subFunc(self,match:re.Match):
        word = match.group(1)
        url = match.group(2)
        pic_block = PictureBlock(word=word,url=url,text=match.group())
        replace_name = self.block.register(pic_block) # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):
            
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text       
        new_text = re.sub(self.RE,self.subFunc,text)
        
        self.parser.match(self.block,new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block.sub_blocks[0].input['text'] = text
            self.block = self.block.sub_blocks[0]
            
        root.addBlock(self.block)
        
class PictureBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
        
class ReferenceHandler(Handler):
    # 处理引用
    # [1](abc)
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        # 匹配嵌套 + 忽略末尾多余 )
        
        # Typora               r'\[([^\[\]]*?)\]\((.*?)\)'
        # Markdown All in One  ...
        self.RE = re.compile(r"""(
            \[([^\[\]]*?)\]\((.*?)\)|
            <((?:[a-zA-z@:\.\/])+?)>
        )""",re.VERBOSE)  

    def subFunc(self,match:re.Match):
        word = match.group(2)
        url = match.group(3)
        # <> 的匹配
        if url == None:
            url = match.group(4)
            word = url
        ref_block = ReferenceBlock(word=word,url=url)
        replace_name = self.block.register(ref_block) # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):

        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE,self.subFunc,text)

        self.parser.match(self.block,new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block.sub_blocks[0].input['text'] = text
            self.block = self.block.sub_blocks[0]
        root.addBlock(self.block)
        
class ReferenceBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)     


class SpecialTextHandler(Handler):
    # 处理特殊字符
    # 不考虑 * 的多级嵌套

    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r"""(
            \*{3}(.+?)\*{3}|                           # 粗体+斜体
            \*{2}_(.+?)_\*{2}|                         # 粗体+斜体
            \*{2}(.+?)\*{2}|                           # 粗体
            _(.+?)_|                                   # 斜体
            \*(.+?)\*|                                 # 斜体
            ~~(.+?)~~|                                 # 删除线
            ``(.+?)``|                                 # 高亮 
            `(.+?)`                                   # 高亮                
        )""", re.VERBOSE)
        self.groupid_tag = {
            2: 'bold+italics',
            3: 'bold+italic',
            4: 'bold',
            5: 'italic',
            6: 'italic',
            7: 'delete',
            8: 'highlight',
            9: 'highlight'
        }

    def subFunc(self,match:re.Match):
        
        for k,v in self.groupid_tag.items():
            if match.group(k):
                word = match.group(k)
                tag = v
                break
        special_text_block = SpecialTextBlock(word=word,tag=tag)
        replace_name = self.block.register(special_text_block) # 注册并替换名字
        return replace_name

    def __call__(self, root: Block, text: str):
            
        self.block = ComplexBlock(text=text)
        # 替换所有匹配项并重新解析new_text
        new_text = re.sub(self.RE,self.subFunc,text)
        
        self.parser.match(self.block,new_text)
        # 单匹配去掉外层 ComplexBlock
        if len(self.block.sub_blocks) == 1:
            self.block.sub_blocks[0].input['text'] = text
            self.block = self.block.sub_blocks[0]
        root.addBlock(self.block)
        
        
        
class SpecialTextBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class TableHandler(Handler):
    # 处理表格
    # 不想支持原生表格...
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        self.RE = re.compile(r'^\|(?: *:?-{1,}:? *\|)+')
        

    def __call__(self, root: Block, text: str):
        # 判断对齐方式
        lines = text.split('|')[1:-1]
        alignments = []
        for line in lines:
            if re.search(r':-+:',line):
                alignments.append('center')
            elif re.search(r'-:',line):
                alignments.append('right')
            else:
                alignments.append('left')
        root.addBlock(TableBlock(text=text,alignments=alignments))

class TableBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class TextHandler(Handler):
    # 处理常规文本
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
        
    def match(self, text:str):  
        return True
    
    def __call__(self, root: Block, text: str):
        
        global CONTAINER
        RE = re.compile(r'({-%.*?%-})')
        split_strings = RE.split(text)

        count = 0
        for string in split_strings:
            # 正常文本字符
            if count % 2 == 0:
                if string:
                    root.addBlock(TextBlock(word=string,text=text))
            else:
                id = string[3:-3]
                try:
                    class_object:Block = CONTAINER[id]
                    class_object.restore(TextBlock)
                    root.addBlock(class_object)
                except:
                    # print(id)
                    # print(CONTAINER)
                    # 由于在解析过程中中间变量使用了{-%.*?%-}的格式进行代替
                    # 所以如果原本的Markdown输入中就包含类似的 {-%asdjkl%-}文字则会出现无法找到的情况
                    # 所以做一个try exception,这种情况当成文字处理
                    root.addBlock(TextBlock(word=string,text=text))
            count += 1
        
class TextBlock(Block):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


def buildBlockParser():
    # block parser 用于逐行处理文本, 并将结果解析为一颗未优化的树
    block_parser = BlockParser()
    block_parser.register(EmptyBlockHandler(block_parser), 'empty', 100)
    block_parser.register(EscapeCharacterHandler(block_parser), 'escape', 99)
    block_parser.register(ExtensionBlockHandler(block_parser), 'extension', 98)
    block_parser.register(SplitBlockHandler(block_parser), 'split', 95)
    block_parser.register(HierarchyIndentHandler(block_parser), 'indent', 90)
    block_parser.register(CodeBlockHandler(block_parser), 'code', 80)
    block_parser.register(HashHeaderHandler(block_parser), 'hashheader', 70)
    block_parser.register(TaskListHandler(block_parser), 'tlist', 50)
    block_parser.register(OListHandler(block_parser), 'olist', 40)
    block_parser.register(UListHandler(block_parser), 'ulist', 30)
    block_parser.register(QuoteHandler(block_parser), 'quote', 20)
    block_parser.register(PictureHandler(block_parser), 'picture', 15)
    block_parser.register(ReferenceHandler(block_parser), 'reference', 10)
    block_parser.register(SpecialTextHandler(block_parser), 'specialtext', 5)
    block_parser.register(TableHandler(block_parser), 'specialtext', 4)
    block_parser.register(TextHandler(block_parser), 'text', 0)
    return block_parser
