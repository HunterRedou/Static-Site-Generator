from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from delimiter import text_to_textnodes, text_to_children

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_mark = markdown.strip()
    
    node_block = []
    current_block = []
    
    for line in new_mark.split('\n'):
        if line.strip().startswith('#'):
            if current_block:
                node_block.append("\n".join(current_block))
                current_block = []
            node_block.append(line.lstrip())
        elif line.strip() == '':
            if current_block:
                node_block.append('\n'.join(current_block))
                current_block = []
        else:
            current_block.append(line.lstrip())
    if current_block:
        node_block.append('\n'.join(current_block))
        
    return node_block


def block_to_block_type(markdown_block):
    if markdown_block.startswith('#'):
        count = 0
        for mark in markdown_block:
            if mark == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6:
            return BlockType.HEADING
        
    if markdown_block.startswith('```') and markdown_block.endswith('```'):
        return BlockType.CODE
    
    lines = markdown_block.split('\n')
    
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    is_ordered_list = True
    
    for i, line in enumerate(lines):
        expec = f'{i+1}. '
        if not line.startswith(expec):
            is_ordered_list = False
            break
        
        if is_ordered_list and lines:
            return BlockType.ORDERED_LIST
        
    
    
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    parent_node = HTMLNode("div", None)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            para_node = HTMLNode("p", None)
            para_space = block.replace("\n", " ").strip()
            para_node.children = text_to_children(para_space)
            children.append(para_node)
        elif block_type == BlockType.HEADING:
            lines = block.split('\n')
            
            
            for line in lines:
                line = line.strip()
                if not line.startswith('#'):
                    continue
                
                
            count = 0
            for head in line:
                if head == "#":
                    count += 1
                else:
                    break
                    
            content = line[count:].lstrip()
            
            head_node = HTMLNode(f'h{count}', None)
            head_node.children = text_to_children(content)
            children.append(head_node)
            
        elif block_type == BlockType.CODE:
            
            lines = block.strip().split("\n")
            code_con = "\n".join(lines[1:-1])
            if not code_con.endswith("\n"):
                code_con += "\n"
            
            code_node = HTMLNode("code", None)
            code_node.children = [text_node_to_html_node(TextNode(code_con, TextType.TEXT))]
            
            pre_node = HTMLNode("pre", None)
            pre_node.children = [code_node]
            children.append(pre_node)
        elif block_type == BlockType.QUOTE:
            lines = block.strip().split("\n")
            quot_con = "\n".join([line.strip()[1:].strip() if line.strip().startswith(">") else line.strip() for line in lines])
            quot_node = HTMLNode("blockquote", None)
            quot_node.children = text_to_children(quot_con)
            children.append(quot_node)
        elif block_type == BlockType.UNORDERED_LIST:
            ul_node = HTMLNode("ul", None)
            list_unor = []
            
            lines = block.strip().split("\n")
            for line in lines:
                if not line.strip():
                    continue
                
                unor_con = line.strip()
                if unor_con.startswith("- "):
                    unor_con = unor_con[2:]
                
                li_node = HTMLNode("li", None)
                li_node.children = text_to_children(unor_con)
                list_unor.append(li_node)
            ul_node.children = list_unor
            children.append(ul_node)
        elif block_type == BlockType.ORDERED_LIST:
            ol_node = HTMLNode("ol", None)
            list_ol = []
            
            lines = block.strip().split("\n")
            for line in lines:
                
                if not line.strip():
                    continue
                
                ol_con = line.strip()
                ol_parts = ol_con.split(". ", 1)
                if len(ol_parts) > 1 and ol_parts[0].isdigit():
                    ol_con = ol_parts[1]
                
                li_node = HTMLNode("li", None)
                li_node.children = text_to_children(ol_con)
                list_ol.append(li_node)
                
            ol_node.children = list_ol
            children.append(ol_node)     
             
    parent_node.children = children
    return parent_node
        
def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith('# '):
            return line[2:].strip()
    
    raise Exception("No h1 Header found")

def generate_page(from_path, temp_path, dest_path):
    with open(from_path) as fp:
        path_fp = fp.read()
    with open(temp_path) as tp:
        temp_tp = tp.read()
        
    print(f'Generating page from {from_path} to {dest_path} using {temp_path}')
    
    convert_md = markdown_to_html_node(path_fp)
    next_convert = convert_md.to_html()
    title = extract_title(path_fp)
    html_title = temp_tp.replace("{{ Title }}", title)
    final_html = html_title.replace("{{ Content }}", next_convert)
    
    import os
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as dp:
        dp.write(final_html)
    
    
    
                
            
    