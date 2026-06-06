#!/usr/bin/env python3
import os

# Configuration
IMAGE_DIR = "image"
WALLPAPER_DIR = os.path.join(IMAGE_DIR, "wallpaper")
MISC_DIR = os.path.join(IMAGE_DIR, "Misc")
LIVE_DIR = "live"
README_FILE = "README.md"

def generate_html_table(folder_path, relative_prefix):
    if not os.path.exists(folder_path):
        return ""
    
    # Filter for images and sort them alphabetically
    valid_exts = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
    files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(valid_exts)])
    
    if not files:
        return "<p>No wallpapers here yet!</p>"
    
    html = "<table>\n"
    for i in range(0, len(files), 4):
        html += "<tr>\n"
        for j in range(4):
            if i + j < len(files):
                # Clean up paths to use forward slashes for cross-platform Markdown compatibility
                img_path = os.path.join(relative_prefix, files[i+j]).replace("\\", "/")
                html += f'<td><img src="{img_path}" width="200"/></td>\n'
            else:
                html += "<td></td>\n"
        html += "</tr>\n"
    html += "</table>"
    return html

def generate_live_wallpapers():
    # Looks for matching .gif and .mp4 pairs in the live folder
    if not os.path.exists(LIVE_DIR):
        return "| Preview | File |\n|---------|------|\n"
    
    files = os.listdir(LIVE_DIR)
    mp4_files = sorted([f for f in files if f.lower().endswith('.mp4')])
    
    table_rows = ""
    for mp4 in mp4_files:
        base_name = os.path.splitext(mp4)[0]
        # Look for a matching gif preview, fallback to a placeholder if missing
        gif = f"{base_name}.gif" if f"{base_name}.gif" in files else ""
        preview = f"![{base_name}]({LIVE_DIR}/{gif})" if gif else "No preview"
        table_rows += f"| {preview} | [{mp4}]({LIVE_DIR}/{mp4}) |\n"
        
    return f"| Preview | File |\n|---------|------|\n{table_rows}"

def build_structure_tree():
    # Dynamically builds the folder structure view based on what exists in Misc
    misc_folders = []
    if os.path.exists(MISC_DIR):
        misc_folders = sorted([f for f in os.listdir(MISC_DIR) if os.path.isdir(os.path.join(MISC_DIR, f))])
    
    tree = "Wallpaper/\n├── image/\n│   ├── wallpaper/     \u2190 active wallpapers\n│   └── Misc/      \u2190 Misc wallpapers categorized in folders\n"
    for i, folder in enumerate(misc_folders):
        connector = "│       └── " if i == len(misc_folders) - 1 else "│       ├── "
        tree += f"{connector}{folder}/\n"
    tree += "|\n└── live/              \u2190 live/video wallpapers"
    return tree

def main():
    print("Generating README.md...")
    
    # 1. Structure Tree
    structure_tree = build_structure_tree()
    
    # 2. Active Wallpapers Table
    active_table = generate_html_table(WALLPAPER_DIR, "image/wallpaper")
    
    # 3. Live Wallpapers Table
    live_table = generate_live_wallpapers()
    
    # 4. Misc Dropdowns
    misc_sections = ""
    if os.path.exists(MISC_DIR):
        misc_folders = sorted([f for f in os.listdir(MISC_DIR) if os.path.isdir(os.path.join(MISC_DIR, f))])
        for folder in misc_folders:
            folder_path = os.path.join(MISC_DIR, folder)
            table_html = generate_html_table(folder_path, f"image/Misc/{folder}")
            misc_sections += f"<details>\n<summary>{folder}</summary>\n{table_html}\n</details>\n\n"

    # Static Template
    readme_content = f"""# 🖼 Wallpapers

A personal wallpaper collection — backup and dump.

> **Clone:**
> ```bash
> git clone git@github.com:IdontKNOWcodingREALLY/wallpapers.git /mnt/hdd/Pictures/Wallpaper
> ```

---

## 📁 Structure

```
{structure_tree}
```

---
## 🎬 Live Wallpapers

{live_table}

---

## 🖼 Active Wallpapers

{active_table}

---

## ✨ Misc

{misc_sections.strip()}

---

## 📖 Usage

### Clone on a new machine
```bash
git clone git@github.com:IdontKNOWcodingREALLY/wallpapers.git /mnt/hdd/Pictures/Wallpaper
```

### Add a new wallpaper
```bash
cd /mnt/hdd/Pictures/Wallpaper
cp /path/to/new.jpg image/wallpaper/
python3 generate_readme.py
git add -A
git commit -m "Add new wallpaper"
git push
```

### Move a wallpaper to Misc
```bash
mv image/wallpaper/unwanted.jpg image/Misc/
python3 generate_readme.py
git add -A
git commit -m "Reject unwanted.jpg"
git push
```

### Add a new live wallpaper
Edit `.gitignore` to include the new file:
```gitignore
!live/new-wallpaper.mp4
```
Then:
```bash
python3 generate_readme.py
git add -A
git commit -m "Add new live wallpaper"
git push
```

### Update README after adding new wallpapers
```bash
python3 generate_readme.py
```
"""

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    print("README.md updated successfully!")

if __name__ == "__main__":
    main()
