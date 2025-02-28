import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.google.com"})
        self.assertEqual(node.__repr__(), "HTMLNode(a, Click me, children: None, {'href': 'https://www.google.com'})")

    
    def test_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.__repr__(), "HTMLNode(None, None, children: None, None)")
    
    
    def test_props_to_html(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me</a>')


    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_to_html_with_no_children(self):
        childless_node = ParentNode("p", [])
        self.assertEqual(
            childless_node.to_html(),
            "<p></p>"
        )

    
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "I'm a baby")
        child2 = LeafNode(None, "hear me roar")
        child3 = LeafNode("em", "STRONGBOI")
        child4 = LeafNode("i", "I'm going to betray everyone")
        busy_parent = ParentNode("h3", [child1, child2, child3, child4])
        self.assertEqual(
            busy_parent.to_html(),
            "<h3><span>I'm a baby</span>hear me roar<em>STRONGBOI</em><i>I'm going to betray everyone</i></h3>"
        )

if __name__ == "__main__":
    unittest.main()
