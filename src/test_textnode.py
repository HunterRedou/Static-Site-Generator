import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a test node", TextType.BOLD_TEXT)
        self.assertEqual(node,node2)
    def test_url(self):
        url_node = TextNode("This is the ulti test", TextType.NORMAL_TEXT, "www.youtube.com/ZzTooly")
        url_node2 = TextNode("This is the ulti test", TextType.NORMAL_TEXT, "www.youtube.com/ZzTooly")
        self.assertEqual(url_node, url_node2)
    def test_dif(self):
        dif_node = TextNode("This is a dif test", TextType.ITALIC_TEXT, "www.twitch.com/Zztooly")
        dif_node2 = TextNode("This is a differant Test", TextType.LINK_TEXT, "www.bootdev.com/login")
        self.assertNotEqual(dif_node, dif_node2)
    def test_non(self):
        non_node = TextNode("This is the same Test", TextType.LINK_TEXT, None)
        non_node2 = TextNode("This is the same Test", TextType.LINK_TEXT, None)
        self.assertEqual(non_node, non_node2)
        
        
if __name__ == "__main__":
    unittest.main()