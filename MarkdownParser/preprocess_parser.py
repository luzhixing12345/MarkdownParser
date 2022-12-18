

from .base_class import Parser,Handler
import re
from .block_parser import HTMLBlock
from .base_class import CONTAINER

class PreprocessParser(Parser):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, data:str):
        self._sort()
        # 按优先级逐步执行相应处理方法
        for method in self._handlers:
            data = method['object'](data)

        lines = data.split('\n')
        return lines

    def getHtmlPosition(self):
        return self.preprocess_parser['html'].match_results

class TextCharacterHander(Handler):

    def __init__(self, tabsize: int) -> None:
        super().__init__()
        self.tabsize = tabsize

    def __call__(self, text: str):

        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = text.expandtabs(tabsize=self.tabsize)
        text = re.sub(r'(?<!\\)\<!--[\s\S]*?--\>','',text)                # 去除注释
        
        # text = re.sub(r'^[ ]{1,3}[^ ]', '', text, flags=re.M) # 每行开头四个以下空格去掉
        # text = re.sub(r'[ ]{1,}$', '', text, flags=re.M)      # 每行结尾空格去掉
        return text


class HTMLLabelHandler(Handler):

    # TODO: 标签不自闭合的处理
    
    def __init__(self) -> None:
        
        super().__init__()

        self.RE = re.compile(r"""
            (<div[\s\S]*?>[\s\S]*?<\/div>|         # div
            <span[\s\S]*?>[\s\S]*?<\/span>|        # span
            <p[\s\S]*?>[\s\S]*?<\/p>|            # p
            <image[\s\S]*?>(?:<\/image>)?|   # image
            <iframe[\s\S]*?>[\s\S]*?<\/iframe>|    # iframe
            <br\/?>|
            <kbd>[\s\S]*?</kbd>
            )""",re.VERBOSE)

    def __call__(self, text: str):
        

        
        def subFunc(match):
            global CONTAINER
            src = match.group(0)
            block = HTMLBlock(text=src,word=src)
            return CONTAINER.register(block)
        
        text = re.sub(self.RE,subFunc,text)
        text = re.sub(r'^[\n]+', '', text)                    # 去除开头连续空换行
        # text = re.sub(r'[\n]+$', '', text)                    # 去除结尾连续空换行
        # text = re.sub(r'[\n]{3,}', '\n\n', text)              # 去除连续换行
        # print(text)
        return text


def buildPreprocessParser(tabsize):
    # preprocess parser 用于预处理空行/注释/HTML标签
    preprocess_parser = PreprocessParser()
    preprocess_parser.register(TextCharacterHander(tabsize), priority=100)
    preprocess_parser.register(HTMLLabelHandler(), priority= 80)
    return preprocess_parser
