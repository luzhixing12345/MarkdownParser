
import markdown
import MarkdownParser

import sys


def main():
    
    with open('test.md','r',encoding='utf-8') as f:
        text = f.read()
        
    x = int(sys.argv[1])
    if x == 1:
        html = MarkdownParser.parse(text)
    else:
        html = markdown.markdown(text)
    # print(html)
    

    
if __name__ == "__main__":
    main()