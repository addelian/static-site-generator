import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.google.com"})
        self.assertEqual(node.__repr__(), "HTMLNode(a, Click me, children: None, {'href': 'https://www.google.com'})")

    
    def test_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.__repr__(), "HTMLNode(None, None, children: None, None)")
    
    
    def test_props_to_html(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.google.com", "target": "_blank"})
        print(node.to_html())
        self.assertEqual(node.to_html(), " href=https://www.google.com target=_blank")


if __name__ == "__main__":
    unittest.main()
