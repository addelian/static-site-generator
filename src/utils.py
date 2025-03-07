import re

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
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown syntax - do you have one too few or too many delimiters?")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def parse_node(node: TextNode, extract_func, text_type: TextType, ep):
    nodes = []
    if node.text_type != TextType.TEXT:
        nodes.append(node)
        return nodes
    extracted_params = extract_func(node.text)
    if extracted_params == []:
        nodes.append(node)
        return nodes
    text_to_split = node.text
    for i in range(len(extracted_params)):
        text, url = extracted_params[i]
        sections = text_to_split.split(f"{ep}[{text}]({url})")
        if sections[0] != "":
            text_node = TextNode(sections[0], TextType.TEXT)
            nodes.append(text_node)
        nodes.append(TextNode(text, text_type, url))
        if i < len(extracted_params) - 1:
            text_to_split = sections[1]
        else: 
            if sections[1] != "":
                text_node = TextNode(sections[1], TextType.TEXT)
                nodes.append(text_node)
    return nodes

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(parse_node(node, extract_markdown_images, TextType.IMAGE, '!'))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(parse_node(node, extract_markdown_links, TextType.LINK, ''))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [node], "`", TextType.CODE
                        ), "**", TextType.BOLD
                    ), "_", TextType.ITALIC
                )
            )
        )
    return new_nodes