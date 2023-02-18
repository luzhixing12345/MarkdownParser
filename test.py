
import MarkdownParser
import sys

# usage:
# python test.py <FILE_NAME>
#
# python test.py ./testfiles/test1.md

html = MarkdownParser.parseFile(sys.argv[1])

with open('./template.html','r',encoding='utf-8') as f:
    html_template = f.read()
    
html_template = html_template.replace('html-scope',html)

with open('./index.html','w',encoding='utf-8') as f:
    f.write(html_template)