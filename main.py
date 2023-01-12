
import MarkdownParser


def main():
    
    html = MarkdownParser.parse('# Hello World')
    print(html)

    html = MarkdownParser.parseFile('./README.md')
    print(html)

if __name__ == "__main__":
    main()
