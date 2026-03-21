import os
import glob

FAVICON_TAG = "<link rel=\"icon\" type=\"image/svg+xml\" href=\"data:image/svg+xml,<svg viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'><circle cx='20' cy='20' r='18' fill='%23155EEF'/><circle cx='20' cy='20' r='9' fill='none' stroke='%23fff' stroke-width='2.5'/><path d='M14 20 A6 6 0 0 1 26 20' fill='none' stroke='%23fff' stroke-width='2.5' stroke-linecap='round'/><polyline points='24,17 26,20 23,21' fill='none' stroke='%23fff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>\">\n</head>"

pages_dir = r"c:\Users\dixit001\OneDrive\Desktop\odoo\plm-eco-system\frontend\pages"

for filepath in glob.glob(os.path.join(pages_dir, "*.html")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove existing favicon if present
    import re
    content = re.sub(r'<link rel="icon"[^>]+>', '', content)
    
    if "</head>" in content:
        content = content.replace("</head>", FAVICON_TAG)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Added favicon to {os.path.basename(filepath)}")
