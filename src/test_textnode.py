import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    
    def test_not_eq(self):
        node = TextNode("Check me", TextType.TEXT)
        node_b = TextNode("Check me", TextType.BOLD)
        self.assertEqual(node.text, node_b.text)
        self.assertNotEqual(node, node_b)
    
    
    def test_url(self):
        node = TextNode("New node", TextType.ITALIC, "https://plots.club")
        self.assertEqual(node.url, "https://plots.club")


    def test_default_url(self):
        node = TextNode("Empty Earl", TextType.CODE)
        node_explicit = TextNode("REALLY Empty Earl", TextType.CODE, None)
        self.assertEqual(node.url, None)
        self.assertEqual(node_explicit.url, None)


if __name__ == "__main__":
    unittest.main()