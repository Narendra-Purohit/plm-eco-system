import os, glob

pages_dir = r"c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages"
for filepath in glob.glob(os.path.join(pages_dir, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content.replace(
        "localStorage.getItem('token')",
        "localStorage.getItem('access_token')"
    )
    
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated", os.path.basename(filepath))
