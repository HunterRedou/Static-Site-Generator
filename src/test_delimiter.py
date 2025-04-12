import unittest

from textnode import TextType, TextNode
from delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is text to test **bold** statement", TextType.TEXT)
        bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            bold_nodes,
            [
                TextNode("This is text to test ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" statement", TextType.TEXT)
            ]
        )
    def test_delimiter_italic(self):
        node = TextNode("This is text to test _italic_ statement", TextType.TEXT)
        italic_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            italic_nodes,
            [
                TextNode("This is text to test ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" statement", TextType.TEXT)
            ]
        )
    def test_delimiter_double(self):
        node = TextNode("This is text to `code1` test `code2` statement", TextType.TEXT)
        code_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            code_nodes,
            [
                TextNode("This is text to ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" test ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" statement", TextType.TEXT)
                
            ]
        )
    def test_delimiter_raise(self):
        node = TextNode("This is text to **bold test statement", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual(str(context.exception), "Second Delimiter not found")
    def test_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_markdown_link(self):
        matches_link = extract_markdown_links(
            "This is text with a link [ZzTooly on YT](https://www.youtube.com/@Zztooly) and [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("ZzTooly on YT", "https://www.youtube.com/@Zztooly"), ("to boot dev", "https://www.boot.dev")], matches_link)