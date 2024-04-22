import MarkdownParser
import unittest
import os


class TestMyMdParser(unittest.TestCase):
    def test_parse_heading(self):
        self.maxDiff = None
        test_id = 28
        md_root_path = f"./testfiles/md"
        html_root_path = f"./testfiles/html"
        MarkdownParser.parse("")
        MarkdownParser.parse("# Heading")
        MarkdownParser.parse_toc("")

        for i in range(1, test_id + 1):
            md_path = os.path.join(md_root_path, f"test{i}.md")
            html_path = os.path.join(html_root_path, f"test{i}.html")
            MarkdownParser.parse_file(md_path)
            html = MarkdownParser.parse_file_toc(md_path)

            # with open(html_path, "w", encoding="utf-8") as f:
            #     f.write(html)

            with open(html_path, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), html, f"test{i} error")
                
        print("pass")


if __name__ == "__main__":
    unittest.main()
