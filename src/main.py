import os
import shutil
import sys

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import generate_page, generate_pages_recursive


def copy_static_dir(static_dir, public_dir):
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    os.mkdir(public_dir)
    
    for item in os.listdir(static_dir):
        static_item = os.path.join(static_dir, item)
        public_item = os.path.join(public_dir, item)
        
        if os.path.isfile(static_item):
            print(f'Copying file: {static_item} to {public_item}')
            shutil.copy(static_item, public_item)
        else:
            copy_static_dir(static_item, public_item)



def main():
    
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    copy_static_dir("static", "docs")
    
    generate_pages_recursive(
        "./content",
        "./template.html",
        "./docs",
        basepath
    )

    





if __name__ == "__main__":
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    main()
    
     