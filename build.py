import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

# Configuration
DATA_FILE = "novel_data.json"
OUTPUT_DIR = "docs"
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"

def load_chapters():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def build_site():
    # 1. Prepare Output Directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    os.makedirs(os.path.join(OUTPUT_DIR, "chapter"))
    os.makedirs(os.path.join(OUTPUT_DIR, "static"))

    # 2. Copy Static Files
    if os.path.exists(STATIC_DIR):
        for item in os.listdir(STATIC_DIR):
            s = os.path.join(STATIC_DIR, item)
            d = os.path.join(OUTPUT_DIR, "static", item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

    # 3. Setup Jinja2 Environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    
    # 4. Load Data
    chapters = load_chapters()
    chapters.sort(key=lambda x: x['id'])

    # 5. Generate Homepage (index.html)
    print("Generating index.html...")
    template = env.get_template("index.html")
    output = template.render(chapters=chapters, is_static=True)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(output)

    # 6. Generate Chapter Pages
    template = env.get_template("chapter.html")
    for i, chapter in enumerate(chapters):
        print(f"Generating chapter {chapter['id']}...")
        
        prev_chapter = chapters[i-1] if i > 0 else None
        next_chapter = chapters[i+1] if i < len(chapters) - 1 else None
        
        output = template.render(
            chapter=chapter, 
            prev_chapter=prev_chapter, 
            next_chapter=next_chapter,
            is_static=True
        )
        
        # Save as chapter/ID.html
        # Note: GitHub Pages handles folders well, but let's stick to a simple structure.
        # We'll save as docs/chapter/1.html
        with open(os.path.join(OUTPUT_DIR, "chapter", f"{chapter['id']}.html"), "w", encoding="utf-8") as f:
            f.write(output)

    print("Build complete! content is in 'docs/' folder.")

if __name__ == "__main__":
    build_site()
