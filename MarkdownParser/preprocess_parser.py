

from .base_parser import Parser
from typing import List
import re

class Preprocessor(Parser):
    
    def __init__(self) -> None:
        super().__init__()

class TextCharacterHander:
    
    def __init__(self, tabsize:int) -> None:
        self.tabsize = tabsize 

    def __call__(self, text:str):

        text = text.replace("\r\n", "\n").replace("\r","\n") + '\n' # 消除换行符影响
        text = text.expandtabs(tabsize=self.tabsize)                # tab扩展为空格
        text = re.sub(r'[\n]+','\n\n',text)                           # 去除连续换行
        return text.split('\n')


class HTMLLabelHandler:
    # TODO
    # too hard for me ...
    ...

def buildPreprocessParser(tabsize):
    
    preprocess_parser = Preprocessor()
    preprocess_parser.register(TextCharacterHander(tabsize), priority= 100)
    # preprocess_parser.register(HTMLLabelHandler(), priority= 80)
    return preprocess_parser