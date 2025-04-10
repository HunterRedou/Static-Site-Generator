import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_met(self):
        props = {"this": "might work", "maybe": "today"}
        node = HTMLNode("a", "click me", None, props)
        self.assertEqual(node.props_to_html(), ' this="might work" maybe="today"')
    
    def test_the_other(self):
        child_other = HTMLNode("list", "is here")
        props_other = {"theKey": "is in a box deep in the ocean"}
        node_other = HTMLNode("h1", "the test", [child_other], props_other)
        
        self.assertEqual((node_other.tag, node_other.value, len(node_other.children), node_other.props),("h1", "the test", 1, {"theKey": "is in a box deep in the ocean"}))
        
    def test_child(self):
        child_one = HTMLNode("p", "Poly Text")
        child_two = HTMLNode("i", "Italic text")
        parent = HTMLNode("b", None, [child_one, child_two])
        
        self.assertEqual(len(parent.children), 2)
        self.assertIs(parent.children[0], child_one)
        self.assertIs(parent.children[1], child_two)
        
    def test_tag(self):
        tag_the_test = HTMLNode("a")
        
        self.assertEqual((tag_the_test.tag), ("a"))
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node_leaf = LeafNode("p", "First Test!")
        self.assertEqual(node_leaf.to_html(), "<p>First Test!</p>")
    
    def test_leaf_to_html_props(self):
        the_props = {"id": "main_test"}
        node_props = LeafNode("h1", "The props Test", the_props)
        self.assertEqual(node_props.to_html(), '<h1 id="main_test">The props Test</h1>')
        
    def test_leaf_to_html_value(self):
        props_value = {"player": "HunterRedou"}
        node_value = LeafNode("b", None, props_value)
        with self.assertRaises(ValueError) as context:
            node_value.to_html()
            self.assertEqual(str(context.exception), "All leaf nodes must have a value")
            
    def test_leaf_to_html_none(self):
        node_none = LeafNode(None, "The none Test", None)
        self.assertEqual(node_none.to_html(), "The none Test")