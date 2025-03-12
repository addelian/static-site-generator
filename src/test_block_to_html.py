import unittest


from block_to_html import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is [a link](https://www.google.com)

This is another paragraph with _italic_ text and `code` here

"""
        node: LeafNode | ParentNode | HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is <a href="https://www.google.com">a link</a></p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>',
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node: LeafNode | ParentNode | HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    

    def test_quote_block(self):
        md = """> this is a quote
> and dang if it isn't
> one of the best ones
> ever"""
        node: LeafNode | ParentNode | HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote and dang if it isn't one of the best ones ever</blockquote></div>",
        )

    
    def test_heading_block(self):
        md = "### this is an h3!"
        node: LeafNode | ParentNode | HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>this is an h3!</h3></div>",
        )

    
    def test_ordered_list(self):
        md = """1. my order
2. is grand
3. and oh so great"""
        node: LeafNode | ParentNode | HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>my order</li><li>is grand</li><li>and oh so great</li></ol></div>",
        )


    def test_unordered_list(self):
        md = """- my order
- is grand
- and oh so great"""
        node: LeafNode | ParentNode | HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>my order</li><li>is grand</li><li>and oh so great</li></ul></div>",
        )


    def test_big_combined(self):
        md = """# welcome to my page!

This is **bolded** paragraph
text in a p
tag here

This is [a link](https://www.google.com)

And this is ![an image](https://link.to.image)

This is another paragraph with _italic_ text and `code` here

> how about a quote?

1. my
2. ordered
3. list

- my
- unordered
- list

_what if the italics were alone?_

**and how about the bold?**
"""
        node: LeafNode | ParentNode | HTMLNode = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            '<div><h1>welcome to my page!</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is <a href="https://www.google.com">a link</a></p><p>And this is <img src="https://link.to.image" alt="an image"></img></p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><blockquote>how about a quote?</blockquote><ol><li>my</li><li>ordered</li><li>list</li></ol><ul><li>my</li><li>unordered</li><li>list</li></ul><p><i>what if the italics were alone?</i></p><p><b>and how about the bold?</b></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
