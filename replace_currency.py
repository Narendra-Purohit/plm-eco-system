import glob
import os

base = 'c:/Users/Hp/Desktop/PLM/plm-eco-system/frontend/pages/*.html'
files = glob.glob(base)
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    if '$${' in content:
        content = content.replace('$${', '₹${')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1
        print(f"Patched: {os.path.basename(f)}")

print(f"Total files patched: {count}")
