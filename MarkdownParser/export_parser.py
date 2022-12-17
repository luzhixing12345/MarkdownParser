
from .base_class import Parser, Block
import re

class ExportParser(Parser):
    
    def __init__(self) -> None:
        super().__init__()
        with open('./MarkdownParser/template.html','r',encoding='utf-8') as f:
            template_html = f.read()
        self.template_htmls = re.split(r'css-scope|html-scope|js-scope',template_html)
        
        self.css_content = "<link rel='stylesheet' href='./MarkdownParser/css/github.css'/>"
    def __call__(self, tree:Block):
        tree.info()
        html_content = ''
        for sub_block in tree.sub_blocks:
            html_content += sub_block.toHTML()
        print(html_content)
        self.writeToHTML(html_content,self.css_content)
        
    def writeToHTML(self, html_content, css_content='', js_content = ''):
        html = self.template_htmls[0] + css_content + self.template_htmls[1] + html_content + self.template_htmls[2]
        with open('./index.html','w',encoding='utf-8') as f:
            f.write(html)


def buildExportProcessor():
    
    export_parser = ExportParser()
    
    return export_parser