import unittest

from textnode import TextType, TextNode
from delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_empty(self):
        node_empty = TextNode(
            "This is empty text",
            TextType.TEXT,
        )
        new_node_empty = split_nodes_image([node_empty])
        self.assertListEqual(
            [
                TextNode("This is empty text", TextType.TEXT),
            ],
            new_node_empty,
        )
    def test_split_images_one(self):
        node_one = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes_one = split_nodes_image([node_one])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                
            ],
            new_nodes_one,
        )
    def test_split_link(self):
        node_link = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes_link = split_nodes_link([node_link])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes_link,
        )
    def test_split_link_empty(self):
        node_empty = TextNode(
            "This is empty text",
            TextType.TEXT,
        )
        new_node_empty = split_nodes_link([node_empty])
        self.assertListEqual(
            [
                TextNode("This is empty text", TextType.TEXT),
            ],
            new_node_empty,
        )
    def test_split_link_one(self):
        node_one_link = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes_one = split_nodes_link([node_one_link])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                
            ],
            new_nodes_one,
        )
    def test_text_to_textnode(self):
        node = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node,
        )
    def test_text_to_textnode_raise(self):
        
        with self.assertRaises(Exception) as context:
            text_to_textnodes("this is **bold")
            self.assertEqual(str(context.exception), "Second Delimiter not found")
    def test_text_to_textnode_link(self):
        node_link = text_to_textnodes("[ZzTooly](https://youtube.com@ZzTooly)")
        self.assertListEqual(
            [
                TextNode("ZzTooly", TextType.LINK, "https://youtube.com@ZzTooly")
            ],
            node_link,
        )
    def test_text_to_textnode_multi(self):
        node_multi = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            node_multi,
        )
        
    