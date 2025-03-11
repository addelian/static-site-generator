from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block:
            lines = [line.strip() for line in cleaned_block.split("\n")]
            filtered_blocks.append("\n".join(lines))
    return filtered_blocks


def block_to_block_type(text: str):
    # code
    if text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    lines = text.split("\n")
    # heading
    if len(lines) == 1:
        leading_chars = lines[0].split(" ")[0]
        if re.findall(r"^#{1,7}$", leading_chars):
                return BlockType.HEADING
    # quote
    quote = all(map(lambda l: l.startswith(">"), lines))
    if quote:
        return BlockType.QUOTE
    # ul
    ul = all(map(lambda l: l.startswith("- "), lines))
    if ul:
        return BlockType.UNORDERED_LIST
    # ol
    for i in range(len(lines)):
        prefix = lines[i].split(" ")[0]
        if not re.findall(r"^\d*\.$", prefix):
            break
        num = prefix.split(".")[0]
        if not (int(num) == i + 1):
            break
        if i == len(lines) - 1:
            return BlockType.ORDERED_LIST
    # default
    return BlockType.PARAGRAPH
