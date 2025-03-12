import re

from blocks import  BlockType, markdown_to_blocks, block_to_block_type
from utils import text_to_textnodes, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

def markdown_to_html_node(markdown) -> HTMLNode | LeafNode | ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(paragraph_to_html_node(block))
        elif block_type == BlockType.CODE:
            html_nodes.append(code_to_html_node(block))
        elif block_type == BlockType.HEADING:
            html_nodes.append(heading_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(quote_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_nodes.append(ol_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_nodes.append(ul_to_html_node(block))
    return ParentNode("div", html_nodes)


def paragraph_to_html_node(block):
    nodes: list[TextNode] = text_to_textnodes(block)
    nodes_to_extend = []
    for node in nodes:
        node.text = node.text.replace("\n", " ")
        html_node = text_node_to_html_node(node)
        nodes_to_extend.append(html_node)
    return ParentNode("p", nodes_to_extend)


def code_to_html_node(block):
    code_text = ("\n".join(block.split("\n")[1:-1])+"\n")
    code_node = TextNode(code_text, TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(code_node)])


def quote_to_html_node(block):
    nodes: list[TextNode] = text_to_textnodes(block)
    nodes_to_extend = []
    for node in nodes:
        node.text = " ".join(node.text.replace("> ", "").split("\n"))
        html_node = text_node_to_html_node(node)
        nodes_to_extend.append(html_node)
    return ParentNode("blockquote", nodes_to_extend)


def heading_to_html_node(block):
    nodes: list[TextNode] = text_to_textnodes(block)
    nodes_to_extend = []
    for node in nodes:
        heading = re.findall(r"^#{1,6} ", node.text)[0]
        hnum = len(heading) - 1
        node.text = node.text.replace(heading, "")
        html_node = text_node_to_html_node(node)
        nodes_to_extend.append(html_node)
    return ParentNode(f"h{hnum}", nodes_to_extend)


def ol_to_html_node(block):
    nodes: list[TextNode] = text_to_textnodes(block)
    nodes_to_extend = []
    for node in nodes:
        lines = node.text.split("\n")
        for line in lines:
            prefix = re.findall(r"^\d*\. ", line)[0]
            line = line.replace(prefix, "")
            nodes_to_extend.append(LeafNode("li", line))
    return ParentNode("ol", nodes_to_extend)


def ul_to_html_node(block):
    nodes: list[TextNode] = text_to_textnodes(block)
    nodes_to_extend = []
    for node in nodes:
        lines = node.text.split("\n")
        for line in lines:
            line = line.replace("- ", "")
            nodes_to_extend.append(LeafNode("li", line))
    return ParentNode("ul", nodes_to_extend)