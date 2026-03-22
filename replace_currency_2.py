import glob

count = 0
for f in glob.glob('c:/Users/Hp/Desktop/PLM/plm-eco-system/frontend/pages/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = content.replace('>$<', '>₹<').replace('($)', '(₹)')
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        count += 1
        print(f'Fixed html decorators in {f}')
print(f'Done fixing decorators: {count} files')
