import MarkdownParser
import unittest
import os


class TestMyMdParser(unittest.TestCase):
    def test_parse_heading(self):
        self.maxDiff = None
        
        test_nums = len(os.listdir("./testfiles/md"))
        
        md_root_path = f"./testfiles/md"
        html_root_path = f"./testfiles/html"
        MarkdownParser.parse("")
        MarkdownParser.parse("# Heading")
        MarkdownParser.parse_toc("")

        failed_test_ids = []

        for i in range(1, test_nums + 1):
            md_path = os.path.join(md_root_path, f"test{i}.md")
            html_path = os.path.join(html_root_path, f"test{i}.html")
            MarkdownParser.parse_file(md_path)
            html = MarkdownParser.parse_file_toc(md_path)

            # with open(html_path, "w", encoding="utf-8") as f:
            #     f.write(html)

            with open(html_path, "r", encoding="utf-8") as f:
                md_result = f.read()
                if md_result != html: # pragma: no cover
                    print(f"\033[31mtest {i} failed\033[0m")
                    failed_test_ids.append(i)
                else:
                    print(f"\033[32mtest {i} passed\033[0m")

        if len(failed_test_ids) > 0: # pragma: no cover
            print(f"failed test ids: {failed_test_ids}")
            self.assertTrue(False)

        print("all tests passed!")


if __name__ == "__main__":
    unittest.main()
