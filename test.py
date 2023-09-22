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
        MarkdownParser.parse_file("./testfiles/test9.md")
        MarkdownParser.parse_file("./testfiles/test10.md")
        MarkdownParser.parse_file("./testfiles/test11.md")
        MarkdownParser.parse_file("./testfiles/test12.md")
        MarkdownParser.parse_file("./testfiles/test13.md")
        MarkdownParser.parse_file("./testfiles/test14.md")
        MarkdownParser.parse_file("./testfiles/test9.md")
        MarkdownParser.parse_file("./testfiles/test10.md")
        MarkdownParser.parse_file("./testfiles/test11.md")
        MarkdownParser.parse_file("./testfiles/test12.md")
        MarkdownParser.parse_file("./testfiles/test13.md")
        MarkdownParser.parse_file("./testfiles/test14.md")
        MarkdownParser.parse_file("./testfiles/test15.md")
        MarkdownParser.parse_toc("")
        MarkdownParser.parse_file_toc("./testfiles/test9.md")
        MarkdownParser.parse_file_toc("./testfiles/test10.md")
        MarkdownParser.parse_file_toc("./testfiles/test11.md")
        MarkdownParser.parse_file_toc("./testfiles/test12.md")
        MarkdownParser.parse_file_toc("./testfiles/test13.md")
        MarkdownParser.parse_file_toc("./testfiles/test14.md")
        MarkdownParser.parse_file_toc("./testfiles/test15.md")
        MarkdownParser.parse_file_toc("./testfiles/test16.md")
        MarkdownParser.parse_file_toc("./testfiles/test17.md")
        MarkdownParser.parse_file_toc("./testfiles/test18.md")
        MarkdownParser.parse_file_toc("./testfiles/test19.md")


if __name__ == "__main__":
    unittest.main()
