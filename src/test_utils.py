import unittest

from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    
    def test_bold_text(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])


    def test_italic_text(self):
        node = TextNode("This is text with an __italic__ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    
    def test_multiple_nodes(self):
        node = TextNode("This is text with an __italic__ word", TextType.TEXT)
        node2 = TextNode("And then here's __another__ one", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "__", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("And then here's ", TextType.TEXT),
            TextNode("another", TextType.ITALIC),
            TextNode(" one", TextType.TEXT),
        ])

    
    def test_no_change(self):
        node = TextNode("already bolded", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])


    def test_invalid_markdown(self):
        node = TextNode("I have **bad syntax", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    
    def test_invalid_markdown_image_format(self):
        matches = extract_markdown_images(
            "Bad ![image(link.com/here.png)"
        )
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    
    def test_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


    def test_invalid_markdown_link_format(self):
        matches = extract_markdown_links(
            "Bad [link]www.bob.com)"
        )
        self.assertListEqual([], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_trailing_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and more text afterwards", TextType.TEXT)
            ],
            new_nodes,
        )


    def test_split_images_no_separating_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and more text afterwards", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_split_images_no_leading_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and more text afterwards", TextType.TEXT)
            ],
            new_nodes,
        )
    

    def test_split_images_no_images(self):
        node = TextNode(
            "image and another image and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                node
            ],
            new_nodes,
        )

    
    def test_split_images_multiple_nodes(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and more text afterwards",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is yet another text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and more text afterwards", TextType.TEXT),
                TextNode("This is yet another text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and more text afterwards", TextType.TEXT)
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_with_trailing_text(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [link](https://www.boot.dev) and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://www.boot.dev"
                ),
                TextNode(" and more text afterwards", TextType.TEXT)
            ],
            new_nodes,
        )


    def test_split_links_no_separating_text(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com)[link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(
                    "link", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_leading_text(self):
        node = TextNode(
            "[link](https://www.google.com) and another [link](https://www.boot.dev) and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://www.boot.dev"
                ),
                TextNode(" and more text afterwards", TextType.TEXT)
            ],
            new_nodes,
        )
    

    def test_split_links_no_links(self):
        node = TextNode(
            "link and another link and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                node
            ],
            new_nodes,
        )

    
    def test_split_links_with_trailing_text(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [link](https://www.boot.dev) and more text afterwards",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is yet another bit of text with a [link](https://www.yahoo.com) and yet another [link](https://plots.club) and more text afterwards",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://www.boot.dev"
                ),
                TextNode(" and more text afterwards", TextType.TEXT),
                TextNode("This is yet another bit of text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.yahoo.com"),
                TextNode(" and yet another ", TextType.TEXT),
                TextNode(
                    "link", TextType.LINK, "https://plots.club"
                ),
                TextNode(" and more text afterwards", TextType.TEXT)
            ],
            new_nodes,
        ) 


if __name__ == "__main__":
    unittest.main()
