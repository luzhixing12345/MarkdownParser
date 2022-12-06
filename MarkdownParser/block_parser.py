
from .base_parser import Parser


class BlockParser(Parser):
    
    ...
    
    
class EmptyBlockHandler:
    
    def __init__(self) -> None:
        pass
    
def buildBlockParser():
    
    parser = BlockParser()
    parser.register(EmptyBlockHandler(parser), 'empty', 100)
    parser.register(ListIndentHandler(parser), 'indent', 90)
    parser.register(CodeBlockHandler(parser), 'code', 80)
    parser.register(HashHeaderHandler(parser), 'hashheader', 70)
    parser.register(SetextHeaderHandler(parser), 'setextheader', 60)
    parser.register(HRHandler(parser), 'hr', 50)
    parser.register(OListHandler(parser), 'olist', 40)
    parser.register(UListHandler(parser), 'ulist', 30)
    parser.register(BlockQuoteHandler(parser), 'quote', 20)
    parser.register(ReferenceHandler(parser), 'reference', 15)
    parser.register(ParagraphHandler(parser), 'paragraph', 10)
    
    return block_parser