import os, re
dir_path = r'c:\Users\Hp\Desktop\PLM\plm-eco-system\frontend\pages'
files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('.html')]

count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # We will replace the non-clickable ❌ with a clickable one
    old_str = '<span class="fs-5">❌</span>'
    
    # We remove whitespace variations if needed, but the basic replace is safer
    if old_str in content:
        new_content = content.replace(
            old_str,
            '<span class="fs-5" style="cursor:pointer;" title="Close" onclick="this.closest(\\\'.alert\\\').classList.add(\\\'d-none\\\'); this.closest(\\\'.alert\\\').classList.remove(\\\'d-flex\\\')">❌</span>'
        )
        if new_content != content:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            count += 1
            print(f"Fixed {os.path.basename(f)}")
        
    # Also handle the formatted version line breaks (Prettier formatted etc)
    # <span class="fs-5">❌</span>
    pat2 = re.compile(r'<span\s+class="fs-5"\s*>❌</span>')
    if pat2.search(content):
        new_content, n = pat2.subn(
            '<span class="fs-5" style="cursor:pointer;" title="Close" onclick="this.closest(\'.alert\').classList.add(\'d-none\'); this.closest(\'.alert\').classList.remove(\'d-flex\')">❌</span>', 
            content
        )
        if n > 0:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            count += 1
            print(f"Fixed {os.path.basename(f)} (regex)")

print(f"Total files fixed: {count}")
