
import MarkdownParser


def main():
    
    with open('testfiles/test.md','r',encoding='utf-8') as f:
        text = f.read()
        
    html = MarkdownParser.parse(text)
    print(html)

    
if __name__ == "__main__":
    main()