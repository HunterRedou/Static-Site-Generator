import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node_nest = LeafNode("b", "grandchild")
        child_node_nest = ParentNode("span", [grandchild_node_nest])
        parent_node_nest = ParentNode("div", [child_node_nest])
        self.assertEqual(
            parent_node_nest.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        parent_node_child = ParentNode("i", None)
        with self.assertRaises(ValueError) as context:
            parent_node_child.to_html()
            self.assertEqual(str(context.exception), "All parent nodes must have a children value")
    
    def test_to_html_with_no_tag(self):
        child_node_tag = LeafNode("h1", "child_tag")
        parent_node_tag = ParentNode(None, [child_node_tag])
        with self.assertRaises(ValueError) as context:
            parent_node_tag.to_html()
            self.assertEqual(str(context.exception), "All parent nodes must have a tag value")
            
    def test_to_html_with_a_lot_of_childs(self):
        child_one = LeafNode("i", "child_one")
        child_three = LeafNode("h1", "child_three")
        child_two = ParentNode("b", [child_one, child_three])
        child_four = LeafNode("span", "child_four")
        child_five = ParentNode("p", [child_four])
        child_six = ParentNode("link", [child_two, child_five])
        self.assertEqual(
            child_six.to_html(),
            "<link><b><i>child_one</i><h1>child_three</h1></b><p><span>child_four</span></p></link>"
        )
        
    def test_to_html_with_props(self):
        props = {"id": "main test"}
        child_props = LeafNode("i", "props")
        parent_props = ParentNode("link", [child_props], props)
        self.assertEqual(
            parent_props.to_html(),
            "<link><i>props</i></link>"
        )
        
            