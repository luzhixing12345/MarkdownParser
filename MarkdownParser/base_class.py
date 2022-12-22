
import re

class Container:
    # 用于记录全局解析时的中间变量替换
    
    def __init__(self) -> None:
        self._container = {
            # block类名-唯一标识符 : block类对象
            # 
        }
        
        self._counter = 0
        self.__str__ = self.__repr__

    def __repr__(self) -> str:
        
        split_line = '-' * 50 + '\n'
        info = f'Total number: {self._counter}\n\n'
        
        for k,v in self._container.items():
            info += f'[{k}]'.ljust(30)
            if v.input.get('word') != None:
                info += f' < word = ' + v.input['word'] + ' >'
            info += '\n'
        return split_line + info + split_line
        
    def __getitem__(self,key):
        return self._container[key]
    
    def register(self, class_object):
        _name = f'{class_object.__class__.__name__}-{str(self._counter)}'
        self._counter += 1
        self._container[_name] = class_object
        return '{-%' + _name + '%-}'

        
        
CONTAINER = Container()


class Parser:
    
    def __init__(self) -> None:
        self._handlers = [] # 保存所有注册的方法
        self.is_sorted = False
        
    def _sort(self):
        
        # 按照优先级从高到低排序,使得解析时依次调用方法
        self._handlers.sort(key=lambda item: item['priority'], reverse=True)
    
    def __call__(self, *args, **kwargs):
        
        raise NotImplementedError
        
    def __getitem__(self, key):
        for method in self._handlers:
            if method['name'] == key:
                return method['object']
    
    def info(self):
        # 查看所有已注册的方法
        if not self.is_sorted:
            self._sort()
        for method in self._handlers:
            name = method['name']
            class_name = method['object'].__class__.__name__
            priority = method['priority']
            print(f'[{name}]({priority}) : {class_name}')
    
    def register(self, class_object:object, priority:int=0) -> None:
        
        new_method = {
            'priority': priority,
            'object'  : class_object
        }
        
        self._handlers.append(new_method)
        

class Block:
    
    def __init__(self, **kwargs) -> None:
        self.input = kwargs
        # input['text']: 输入的纯文本格式,用于恢复原始信息
        # input['word']: 输入的核心文本信息
        self.sub_blocks = []
        self.block_name = self.__class__.__name__
        self.__repr__ = self.__str__
    
    def register(self, class_object):
        
        global CONTAINER
        return CONTAINER.register(class_object)

    def restore(self, TextBlock):
        # 这里传入 TextBlock 是因为 TextBlock 还未定义
        global CONTAINER
        RE = re.compile(r'({-%.*?%-})')
        split_strings = RE.split(self.input['word'])

        count = 0
        for string in split_strings:
            # 正常文本字符
            if count % 2 == 0:
                if string:
                    self.addBlock(TextBlock(word=string,text=string))
            else:
                id = string[3:-3]
                class_object:Block = CONTAINER[id]
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
        # root.info()
        # 递归输出信息
        
        if self.sub_blocks == []:
            return
        else:
            for block in self.sub_blocks:
                print(' '*4*deep,end='')
                print(f'[{block.__class__.__name__}] {str(block)}')
                block.info(deep+1)
                
    def printInfo(self, deep: int=0) -> str:
        # print(root.printInfo())
        # 递归输出信息
        output_str = ''
        if self.sub_blocks == []:
            return output_str
        else:
            for block in self.sub_blocks:
                output_str += ' '*4*deep
                output_str += f'[{block.__class__.__name__}] {str(block)}\n'
                output_str += block.printInfo(deep+1)
            return output_str
      
    def toHTML(self):
        # 转换成HTML格式
        content = ''
        for block in self.sub_blocks:
            content += block.toHTML()
        return f"<div class='markdown-body'>{content}</div>"
      
                    
class Handler:
    
    def __init__(self, parser=None) -> None:

        self.RE = None
        self.parser:Parser = parser
        
    def match(self, text: str, *args):
        
        if self.RE == None:
            raise NotImplementedError
                     
        return bool(self.RE.search(text))
        
    def __call__(self, root: Block, text: str):
        
        raise NotImplementedError
    
class Optimizer:
    
    def __init__(self) -> None:
        
        # 优化器针对的Block
        self.target_block_names = []
        self.is_match = False
    
    def __call__(self, root: Block):
        
        raise NotImplementedError