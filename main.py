
import MarkdownParser


def main():
    
    html = MarkdownParser.parseToTree('# Hello World')
    html.info()


if __name__ == "__main__":
    main()
