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

def split_nodes_image(old_nodes):
    nodes = []
   
    
    for old in old_nodes:
        text = old.text
        images = extract_markdown_images(text)
        if not images:
            nodes.append(old)
        else:
            image_alt, image_url = images[0]
            
            image_markdown = f'![{image_alt}]({image_url})'
            
            parts = text.split(image_markdown, 1)
            
            if parts[0]:
                nodes.append(TextNode(parts[0], TextType.TEXT))
            
            nodes.append(TextNode(image_alt, TextType.IMAGES, image_url))
            
            if len(parts) > 1 and parts[1]:
                remain_node = split_nodes_image([TextNode(parts[1], TextType.TEXT)])
                nodes.extend(remain_node)
    
    return nodes
        
def split_nodes_link(old_nodes):
    nodes_link = []
    
    
    for old in old_nodes:
        text = old.text
        links = extract_markdown_links(text)
        if not links:
            nodes_link.append(old)
        else:
            link_alt, link_url = links[0]
            
            link_markdown = f'[{link_alt}]({link_url})'
            
            parts = text.split(link_markdown, 1)
            
            if parts[0]:
                nodes_link.append(TextNode(parts[0], TextType.TEXT))
            
            nodes_link.append(TextNode(link_alt, TextType.LINK, link_url))
            
            if len(parts) > 1 and parts[1]:
                remain_node = split_nodes_link([TextNode(parts[1], TextType.TEXT)])
                nodes_link.extend(remain_node)
    
    return nodes_link

def text_to_textnodes(text):
    final_nodes = [TextNode(text, TextType.TEXT)]
    
    final_nodes = split_nodes_delimiter(final_nodes, "**", TextType.BOLD)
    final_nodes = split_nodes_delimiter(final_nodes, "_", TextType.ITALIC)
    final_nodes = split_nodes_delimiter(final_nodes, "`", TextType.CODE)
    
    final_nodes = split_nodes_image(final_nodes)
    final_nodes = split_nodes_link(final_nodes)
    
    return final_nodes
    
        
        
        
            
    
    
        
        
        
        
            
        
            
            
            
        
        