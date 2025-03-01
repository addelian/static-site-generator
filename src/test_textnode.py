import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTextNodeToHTMLNode(unittest.TestCase):    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")


    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")


    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")    


    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a link node</a>')


    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.imgur.com/dog")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="https://www.imgur.com/dog" alt="This is an image node"></img>')

    
    def test_invalid_type(self):
        node = TextNode("This is invalid", "jazz")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()