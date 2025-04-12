import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            nodes.append(old)
            continue
        
        text = old.text
        
        if delimiter not in text:
            nodes.append(old)
            continue
        
        first_delimiter = text.find(delimiter)
        
        second_delimiter = text.find(delimiter, first_delimiter + len(delimiter))
        
        if second_delimiter == -1:
            raise Exception("Second Delimiter not found")
        
        first_text = text[:first_delimiter]
        second_text = text[first_delimiter + len(delimiter):second_delimiter]
        third_text = text[second_delimiter + len(delimiter):]
        
        if first_text:
            nodes.append(TextNode(first_text, TextType.TEXT))
        
        nodes.append(TextNode(second_text, text_type))
        
        if third_text:
            after_text = TextNode(third_text, TextType.TEXT)
            after_texts = split_nodes_delimiter([after_text], delimiter, text_type)
            nodes.extend(after_texts)
        
    return nodes
            
            
def extract_markdown_images(text):
    match_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match_images

def extract_markdown_links(text):
    match_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match_links

def split_nodes_images(old_nodes):
    nodes = []
    
    for old in old_nodes:
        
        
        
        
            
        
            
            
            
        
        