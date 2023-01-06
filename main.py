
import MarkdownParser


def main():
    
    html = MarkdownParser.parse('# Hello World')
    print(html)


if __name__ == "__main__":
    main()
