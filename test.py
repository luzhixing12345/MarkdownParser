

import MarkdownParser
import unittest


class TestMyMdParser(unittest.TestCase):

    def test_parse_heading(self):
        MarkdownParser.parse("")
        MarkdownParser.parse("# Heading")
        MarkdownParser.parseFile("./testfiles/test1.md")
        MarkdownParser.parseFile("./testfiles/test2.md")
        MarkdownParser.parseFile("./testfiles/test3.md")
        MarkdownParser.parseFile("./testfiles/test4.md")
        MarkdownParser.parseFile("./testfiles/test5.md")
        MarkdownParser.parseFile("./testfiles/test6.md")
        MarkdownParser.parseFile("./testfiles/test7.md")
        MarkdownParser.parseFile("./testfiles/test8.md")
        MarkdownParser.parse_withtag("")
        MarkdownParser.parseFile_withtag("./testfiles/test9.md")
        MarkdownParser.parseFile_withtag("./testfiles/test10.md")
        MarkdownParser.parseFile_withtag("./testfiles/test11.md")
