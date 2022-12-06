

from typing import List,Dict

class Parser:
    
    def __init__(self) -> None:
        
        self._handlers : List[Dict] = [] # 保存所有注册的方法
        
    
    def _sort(self):
        
        # 按照优先级从高到低排序,使得解析时依次调用方法
        self._handlers.sort(key=lambda item: item['priority'], reverse=True)
    
    def __call__(self, data):
        
        # 按优先级逐步执行相应处理方法
        # 前后方法的输入和输出应保持一致
        for method in self._handlers:
            data = method['object'](data)
            
        return data
    
    def __getitem__(self, key):
        for method in self._handlers:
            if method['name'] == key:
                return method['object']
    
    def register(self, class_object:object, name:str, priority:int) -> None:
        
        new_method = {
            'name'    : name,
            'priority': priority,
            'object'  : class_object
        }
        self._handlers.append(new_method)
        