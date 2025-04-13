import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node, extract_title

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_single(self):
        md_single = """
        This is a single _Italic_Line
        """
        block_single = markdown_to_blocks(md_single)
        self.assertEqual(
            block_single,
            [
                "This is a single _Italic_Line"
            ],
        )
    def test_markdown_to_massive(self):
        md_massiv = """
        -first block
        -to first
        
        
        -second block
        -to second
        
        
        
        -third block
        -to third
        """
        block_massiv = markdown_to_blocks(md_massiv)
        self.assertEqual(
            block_massiv,
            [
                "-first block\n-to first",
                "-second block\n-to second",
                "-third block\n-to third",
            ],
        )
    def test_block_type_head(self):
        block = "### test_file"
        test_block = block_to_block_type(block)
        self.assertEqual(BlockType.HEADING, test_block)
    def test_block_type_code(self):
        block_code = "```test_file```"
        test_block = block_to_block_type(block_code)
        self.assertEqual(BlockType.CODE, test_block)
    def test_block_type_quote(self):
        block_quote = ">test file one\n>test file two\n>test file three"
        test_block = block_to_block_type(block_quote)
        self.assertEqual(BlockType.QUOTE, test_block)
    def test_block_type_unord(self):
        block_unord = "- test file one\n- test file two\n- test file three"
        test_block = block_to_block_type(block_unord)
        self.assertEqual(BlockType.UNORDERED_LIST, test_block)
    def test_block_type_ord(self):
        block_ord = "1. test file one\n2. test file two\n3. test file three"
        test_block = block_to_block_type(block_ord)
        self.assertEqual(BlockType.ORDERED_LIST, test_block)
    def test_block_type_para(self):
        block_para = "This is a Paragraph"
        test_block = block_to_block_type(block_para)
        self.assertEqual(BlockType.PARAGRAPH, test_block)
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node_para = markdown_to_html_node(md)
        html = node_para.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node_code = markdown_to_html_node(md)
        html = node_code.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_quoteblock(self):
        md = """
        >This is the quote test
        >whats going to happen
        """
        node_quote = markdown_to_html_node(md)
        html = node_quote.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is the quote test\nwhats going to happen</blockquote></div>"
        )
    def test_headingblock(self):
        md = "#test1\n##two\n###three\n####four\n#####five\n######six"
        node_head = markdown_to_html_node(md)
        html = node_head.to_html()
        self.assertEqual(
            html,
            "<div><h1>test1</h1><h2>two</h2><h3>three</h3><h4>four</h4><h5>five</h5><h6>six</h6></div>"
        )
    def test_unordered_list(self):
        md = """
        - Item 1
        - Item 2
        - Item 3 with **bold** text
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3 with <b>bold</b> text</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
        1. First item
        2. Second item with _italic_ text
        3. Third item with `code` examples
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code> examples</li></ol></div>"
        )
    def test_title_extract(self):
        md = "# Hallo"
        node = extract_title(md)
        self.assertEqual(
            "Hallo", node
        )