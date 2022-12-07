

from .base_class import Parser,Handler
from typing import List
import re


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
        text = re.sub(r'^[\n]+', '', text)                    # 去除开头连续空换行
        text = re.sub(r'[\n]+$', '', text)                    # 去除结尾连续空换行
        text = re.sub(r'[\n]{3,}', '\n\n', text)              # 去除连续换行
        # text = re.sub(r'^[ ]{1,3}[^ ]', '', text, flags=re.M) # 每行开头四个以下空格去掉
        # text = re.sub(r'[ ]{1,}$', '', text, flags=re.M)      # 每行结尾空格去掉
        return text


class HTMLLabelHandler(Handler):

    # TODO: 标签不自闭合的处理
    
    def __init__(self) -> None:
        
        super().__init__()
        div_label    = r'<div [\s\S]*?>([\s\S]*?)<\/div>'
        span_label   = r'<span [\s\S]*?>([\s\S]*?)<\/span>'
        p_label      = r'<p [\s\S]*?>([\s\S]*?)<\/p>'
        image_label  = r'<image [\s\S]*?>[\s\S]*?(<\/image>)?'
        iframe_label = r'<iframe [\s\S]*?>([\s\S]*?)<\/iframe>'
        br_label     = r'<br\/?>'

        self.supported_label = [
            div_label,
            span_label,
            p_label,image_label,iframe_label,br_label
        ]
        
        self.match_results = []

    def __call__(self, text: str):
        
        # 匹配所有疑似html标签的内容,记录其位置
        for label in self.supported_label:
            match_result = re.finditer(re.compile(label),text)
            self.match_results.extend([i.span() for i in match_result])
        return text


def buildPreprocessParser(tabsize):

    preprocess_parser = PreprocessParser()
    preprocess_parser.register(TextCharacterHander(tabsize), 'character', priority=100)
    preprocess_parser.register(HTMLLabelHandler(), 'html', priority= 80)
    return preprocess_parser
