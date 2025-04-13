import os
import shutil

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import generate_page


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
        
    
    copy_static_dir("static", "public")
    
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )

    





if __name__ == "__main__":
        main()
    
     