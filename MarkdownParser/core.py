

from .preprocess_parser import buildPreprocessParser
from .block_parser import buildBlockParser


class Markdown:
    def __init__(self) -> None:
        print("Activate MarkdownParser")
        self.tabsize = 4
        self.build_parser()        
        
    def build_parser(self):
        
        self.preprocess_parser = buildPreprocessParser(self.tabsize)
        self.block_parser = buildBlockParser()

    def parse(self, text:str):
        
        self.lines = self.preprocess_parser(text)
        self.root = self.block_parser(self.lines)
    

def parse(text:str):
    
    assert type(text) == str, "输入应为字符串"
    
    # 空输入
    if not text.strip():
        return ''

    md = Markdown()
    return md.parse(text)