import MarkdownParser
import unittest


class TestMyMdParser(unittest.TestCase):
    def test_parse_heading(self):

        test_id = 21
        MarkdownParser.parse("")
        MarkdownParser.parse("# Heading")
        MarkdownParser.parse_toc("")

        for i in range(1, test_id + 1):
            MarkdownParser.parse_file(f"./testfiles/test{i}.md")
            MarkdownParser.parse_file_toc(f"./testfiles/test{i}.md")


if __name__ == "__main__":
    unittest.main()
