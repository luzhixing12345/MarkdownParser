

from typing import List,Dict


class Parser:
    
    def __init__(self) -> None:
        super().__init__()
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
        
        
        
class Handler:
    
    def __init__(self) -> None:
        super().__init__()
    
    def match(self, *args):
        
        raise NotImplementedError
        
    def __call__(self, *args):

        raise NotImplementedError
    

class Block:
    
    def __init__(self) -> None:
        super().__init__()
        self.sub_blocks = []
        
    def addBlock(self, block):
        self.sub_blocks.append(block)
        
    def getLastBlock(self):
        if len(self.sub_blocks) == 0:
            return None
        else:
            return self.sub_blocks[-1]
        
    def __str__(self):
        return ''
        
    def info(self, deep: int=0):
        # 递归输出信息
        
        if self.sub_blocks == []:
            return
        else:
            for block in self.sub_blocks:
                print(' '*4*deep,end='')
                print('[',block.__class__.__name__,end='')
                print(' ] ' + str(block))
                block.info(deep+1)