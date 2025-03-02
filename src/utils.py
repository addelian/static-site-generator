from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
        

def split_nodes_delimiter(old_nodes: [TextNode], delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        node_parts = old_node.text.split(delimiter)
        if len(node_parts) != 3:
            raise ValueError("invalid markdown syntax - do you have one too few or too many delimiters?")
        new_nodes.extend([
            TextNode(node_parts[0], TextType.TEXT),
            TextNode(node_parts[1], text_type),
            TextNode(node_parts[2], TextType.TEXT)
        ])
    return new_nodes