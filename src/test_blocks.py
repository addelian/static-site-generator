import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_lines(self):
        md = """This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
 

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_code_block(self):
        block = """```
still a
code
block
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)


    def test_not_code_block(self):
        block = "```this is NOT a code block``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    
    def test_heading(self):
        block = "# my cool project readme"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    
    def test_h6_heading(self):
        block = "###### my cool project readme"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    
    def test_not_heading(self):
        block_no_space = "#my cool project readme"
        block_extra_hash = "######## too small!"
        block_type1 = block_to_block_type(block_no_space)
        block_type2 = block_to_block_type(block_extra_hash)
        self.assertEqual(block_type1, BlockType.PARAGRAPH)
        self.assertEqual(block_type2, BlockType.PARAGRAPH)


    def test_quote(self):
        # I'll never forgive VS Code for this
        block = """> bob said hi
> the raven said yo
> bob said ughv
> the raven's no dove"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    

    def test_not_quote(self):
        block = """> bob said hi
the raven said yo
> bob said ughv
> the raven's no dove"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_ul(self):
        block = """- do good things
- make the world sparkle
- destroy VS code for this formatting sin"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    

    def test_not_ul(self):
        block = """- do good things
2. make the world sparkle
- destroy VS code for this formatting sin"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    
    def test_ol(self):
        block = """1. do good things
2. make the world sparkle
3. destroy VS code for this formatting sin"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_not_ol(self):
        block = """1. do good things
two. make the world sparkle
3. destroy VS code for this formatting sin"""
        block2 = """1. do good things
3. make the world sparkle
2. destroy VS code for this formatting sin"""
        block3 = """10. do good things
11. make the world sparkle
12. destroy VS code for this formatting sin"""
        block_type = block_to_block_type(block)
        block_type2 = block_to_block_type(block2)
        block_type3 = block_to_block_type(block3)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        self.assertEqual(block_type2, BlockType.PARAGRAPH)
        self.assertEqual(block_type3, BlockType.PARAGRAPH)
    

    def test_paragraph(self):
        block = "bog frickin standard"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
