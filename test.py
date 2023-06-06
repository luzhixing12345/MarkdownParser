

import MarkdownParser
import unittest


class TestMyMdParser(unittest.TestCase):

    def test_parse_heading(self):
        MarkdownParser.parse("")
        MarkdownParser.parse("# Heading")
        MarkdownParser.parse_file("./testfiles/test1.md")
        MarkdownParser.parse_file("./testfiles/test2.md")
        MarkdownParser.parse_file("./testfiles/test3.md")
        MarkdownParser.parse_file("./testfiles/test4.md")
        MarkdownParser.parse_file("./testfiles/test5.md")
        MarkdownParser.parse_file("./testfiles/test6.md")
        MarkdownParser.parse_file("./testfiles/test7.md")
        MarkdownParser.parse_file("./testfiles/test8.md")
        MarkdownParser.parse_toc("")
        MarkdownParser.parse_file_toc("./testfiles/test9.md")
        MarkdownParser.parse_file_toc("./testfiles/test10.md")
        MarkdownParser.parse_file_toc("./testfiles/test11.md")
