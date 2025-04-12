import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node,node2)
    def test_url(self):
        url_node = TextNode("This is the ulti test", TextType.TEXT, "www.youtube.com/ZzTooly")
        url_node2 = TextNode("This is the ulti test", TextType.TEXT, "www.youtube.com/ZzTooly")
        self.assertEqual(url_node, url_node2)
    def test_dif(self):
        dif_node = TextNode("This is a dif test", TextType.ITALIC, "www.twitch.com/Zztooly")
        dif_node2 = TextNode("This is a differant Test", TextType.LINK, "www.bootdev.com/login")
        self.assertNotEqual(dif_node, dif_node2)
    def test_non(self):
        non_node = TextNode("This is the same Test", TextType.LINK, None)
        non_node2 = TextNode("This is the same Test", TextType.LINK, None)
        self.assertEqual(non_node, non_node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_b(self):
        node_b = TextNode("here is test text", TextType.BOLD)
        html_node_b = text_node_to_html_node(node_b)
        self.assertEqual(html_node_b.tag, "b")
        self.assertEqual(html_node_b.value, "here is test text")
    def test_text_i(self):
        node_i = TextNode("here is italic test text", TextType.ITALIC)
        html_node_i = text_node_to_html_node(node_i)
        self.assertEqual(html_node_i.tag, "i")
        self.assertEqual(html_node_i.value, "here is italic test text")
    def test_text_c(self):
        node_c = TextNode("here is test code", TextType.CODE)
        html_node_c = text_node_to_html_node(node_c)
        self.assertEqual(html_node_c.tag, "code")
        self.assertEqual(html_node_c.value, "here is test code")
    def test_text_l(self):
        node_l = TextNode("here is the first link", TextType.LINK, "www.youtube.com/ZzTooly")
        html_node_l = text_node_to_html_node(node_l)
        props_link = {"href": "www.youtube.com/ZzTooly"}
        self.assertEqual(html_node_l.tag, "a")
        self.assertEqual(html_node_l.value, "here is the first link")
        self.assertEqual(html_node_l.props, props_link)
    def test_text_img(self):
        node_img = TextNode("here should be the image", TextType.IMAGES, "www.youtube.com/ZzTooly")
        html_node_img = text_node_to_html_node(node_img)
        props_img = {"src": "www.youtube.com/ZzTooly", "alt": "here should be the image"}
        self.assertEqual(html_node_img.tag, "img")
        self.assertEqual(html_node_img.value, None)
        self.assertEqual(html_node_img.props, props_img)
        
        
        
        
if __name__ == "__main__":
    unittest.main()