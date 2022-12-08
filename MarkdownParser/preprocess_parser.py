

from .base_class import Parser,Handler
from typing import List
import re
from .block_parser import _container, _counter,HTMLBlock

class PreprocessParser(Parser):

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, text:str):
        text = super().__call__(text)
        lines = text.split('\n')
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
            <br\/?>)"""                              # br
            ,re.VERBOSE)

    def __call__(self, text: str):
        

        
        def subFunc(match):
            global _counter,_container
            src = match.group(0)
            block = HTMLBlock(word = src)
            name = f'{block.__class__.__name__}-{str(_counter)}'
            _container[name] = block
            _counter += 1
            return '{-%' + name + '%-}'
        
        text = re.sub(self.RE,subFunc,text)
        text = re.sub(r'^[\n]+', '', text)                    # 去除开头连续空换行
        text = re.sub(r'[\n]+$', '', text)                    # 去除结尾连续空换行
        text = re.sub(r'[\n]{3,}', '\n\n', text)              # 去除连续换行
        # print(text)
        return text


def buildPreprocessParser(tabsize):

    preprocess_parser = PreprocessParser()
    preprocess_parser.register(TextCharacterHander(tabsize), 'character', priority=100)
    preprocess_parser.register(HTMLLabelHandler(), 'html', priority= 80)
    return preprocess_parser
