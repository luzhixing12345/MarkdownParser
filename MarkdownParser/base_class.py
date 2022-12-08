
import re
from typing import List,Dict


_container = {
    # block类名-唯一标识符 : block类对象    
} # 保存类对象

_counter = 0


class Parser:
    
    def __init__(self) -> None:
        self._handlers : List[Dict] = [] # 保存所有注册的方法
        
    def _sort(self):
        
        # 按照优先级从高到低排序,使得解析时依次调用方法
        self._handlers.sort(key=lambda item: item['priority'], reverse=True)
    
    def __call__(self, data):
        
        self._sort()
        # 按优先级逐步执行相应处理方法
        # 前后方法的输入和输出应保持一致
        for method in self._handlers:
            data = method['object'](data)
            
        return data
    
    def __getitem__(self, key):
        for method in self._handlers:
            if method['name'] == key:
                return method['object']
    
    def info(self):
        # 查看所有已注册的方法
        self._sort()
        for method in self._handlers:
            name = method['name']
            class_name = method['object'].__class__.__name__
            priority = method['priority']
            print(f'[{name}]({priority}) : {class_name}')
    
    def register(self, class_object:object, name:str, priority:int) -> None:
        
        new_method = {
            'name'    : name,
            'priority': priority,
            'object'  : class_object
        }
        
        self._handlers.append(new_method)
        

class Block:
    
    def __init__(self, **kwargs) -> None:
        self.input = kwargs
        # self.input['text'] 一行输入的纯文本格式,用于恢复code block中代码
        self.sub_blocks = []
    
    def register(self, class_object):
        
        global _counter, _container
        _name = f'{class_object.__class__.__name__}-{str(_counter)}'
        _counter += 1
        
        _container[_name] = class_object
        
        return '{-%' + _name + '%-}'

    def restore(self, TextBlock):
        # 这里传入 TextBlock 是因为 TextBlock 还未定义
        global _container
        RE = re.compile(r'({-%.*?%-})')
        split_strings = RE.split(self.input['word'])

        count = 0
        for string in split_strings:
            # 正常文本字符
            if count % 2 == 0:
                if string:
                    self.addBlock(TextBlock(word=string))
            else:
                id = string[3:-3]
                class_object:Block = _container[id]
                class_object.restore(TextBlock)
                self.addBlock(class_object)
            count += 1
    
    def addBlock(self, block):
        
        self.sub_blocks.append(block)

    def __str__(self):
        
        if not self.input:
            return ''
        
        output = '< '
        for k,v in self.input.items():
            if k == 'text':
                continue
            output += f'{k} = \"{v}\" | '
        if output == '< ':
            output = ''
        else:
            output = output[:-3] + ' >'
        return output

    def info(self, deep: int=0):
        # 递归输出信息
        
        if self.sub_blocks == []:
            return
        else:
            for block in self.sub_blocks:
                print(' '*4*deep,end='')
                print(f'[{block.__class__.__name__}] {str(block)}')
                block.info(deep+1)
      
                    
class Handler:
    
    def __init__(self, parser=None) -> None:

        self.RE = None
        self.parser = parser
        
    def match(self, text: str, *args):
        
        if self.RE == None:
            raise NotImplementedError
                     
        return bool(self.RE.search(text))
        
    def __call__(self, root: Block, text: str):
        
        raise NotImplementedError
    
    