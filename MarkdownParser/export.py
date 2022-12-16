
from .base_class import Parser


class ExportParser(Parser):
    
    def __init__(self) -> None:
        super().__init__()
        
    def __call__(self, tree):

        tree.info()


def buildExportProcessor():
    
    export_parser = ExportParser()
    
    return export_parser