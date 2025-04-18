

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        
        if self.tag is None:
            if self.value is not None:
                return self.value
            else:
                raise ValueError("Cannot convert to HTML: tag is None")
        
        result = f'<{self.tag}'
        
        if self.props:
            for prop, value in self.props.items():
                result += f' {prop}="{value}"'
        
        result += ">"
        
        if self.value:
            result += self.value
        
        if self.children:

                result += ''.join(child.to_html() for child in self.children)
        
        result += f'</{self.tag}>'
        return result
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
        
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        
        super().__init__(tag, value, None, props)
        self.value = value
        self.children = None
        
        
    def to_html(self):
        self_closing_tag = {"img", "b", "i", "code", "link"}
        
        if self.tag in self_closing_tag:
            props_html = self.props_to_html() if self.props else ""
            return f'<{self.tag}{props_html}>{self.value}</{self.tag}>'
        
        if not self.value:
            
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None:
            return str(self.value)
        else:
            if not self.props:
                return f'<{self.tag}>{self.value}</{self.tag}>'
            
            result = ""
            for key, value in self.props.items():
                
                result += f' {key}="{value}"'
                
            
            return f'<{self.tag}{result}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.value = None
        self.children = children
        
    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag value")
        elif not self.children:
            raise ValueError("All parent nodes must have a children value")
        else:
            children_html = ''.join(map(lambda child: child.to_html(), self.children))
            return f'<{self.tag}>{children_html}</{self.tag}>'
        