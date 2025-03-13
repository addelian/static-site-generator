import unittest

from page_utils import extract_title


class TestTextNodeToHTMLNode(unittest.TestCase):    
    def test_extract_title(self):
        markdown = "# Hello"
        header = extract_title(markdown)
        self.assertEqual(header, "Hello")


    def test_extract_title_multiple_lines(self):
        markdown = """# Hello world!
        
        ## Introduction
        
        Nice day we're having, huh? These are my cool things:
        
        - pony
        - mip
        - boop
        
        Bye!"""
        header = extract_title(markdown)
        self.assertEqual(header, "Hello world!")

    
    def test_extract_title_missing(self):
        markdown = "## Hello"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
