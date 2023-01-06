

from .preprocess_parser import buildPreprocessParser
from .block_parser import buildBlockParser
from .tree_parser import buildTreeParser
from .export_parser import buildExportProcessor

class Markdown:
    def __init__(self) -> None:
        self.build_parser()        
        
    def build_parser(self):
        
        self.preprocess_parser = buildPreprocessParser()
        self.block_parser = buildBlockParser()
        self.tree_parser = buildTreeParser()
        self.export_processor = buildExportProcessor()

    def parse(self, text:str):
        
        # 去除空行/注释/html标签
        lines = self.preprocess_parser(text)
        
        # 逐行解析,得到一颗未优化的树
        root = self.block_parser(lines)
        # root.info()
        # 优化,得到正确的markdown解析树
        tree = self.tree_parser(root)
        # tree.info()
        # 输出到屏幕 / 导出html文件
        html = self.export_processor(tree)
        # print(html)
        return html
    
    
def parse(text:str):
    
    assert type(text) == str, "输入应为字符串"
    
    # 空输入
    if not text.strip():
        return ''

    md = Markdown()
    return md.parse(text)
