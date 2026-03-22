import requests, sys
API = 'http://127.0.0.1:8000/api'
def p(m): print(m)
r = requests.post(f'{API}/auth/login/', json={'login_id':'admin01', 'password':'PLM@1234'})
if r.status_code != 200: p('Admin login failed: ' + r.text); sys.exit(1)
token = r.json()['access']
headers = {'Authorization': f'Bearer {token}'}

r = requests.get(f'{API}/products/', headers=headers)
prods = r.json()
p1 = prods[0]['id']; p2 = prods[1]['id']
bom_data = {
    'product_id': p1, 'quantity': '1', 'unit': 'EA',
    'components': [{'component_product_id': p2, 'quantity': '5', 'unit': 'EA'}],
    'operations': []
}
r = requests.post(f'{API}/boms/', json=bom_data, headers=headers)
if r.status_code != 201: p('BOM Create failed: ' + r.text); sys.exit(1)
bom_id = r.json()['id']
bom_update = {'components': [{'component_product_id': p2, 'quantity': '10', 'unit': 'EA'}], 'quantity': '2'}
r = requests.patch(f'{API}/boms/{bom_id}/', json=bom_update, headers=headers)
if r.status_code != 200: p('BOM Update failed! BUG STILL PRESENT: ' + r.text); sys.exit(1)
p('✅ BOM Update Fixed!')

eco_data = {'title': 'Test Admin Bypass ECO', 'eco_type': 'product', 'product': p1}
r = requests.post(f'{API}/ecos/', json=eco_data, headers=headers)
eco_id = r.json()['id']
requests.post(f'{API}/ecos/{eco_id}/start/', headers=headers)
r = requests.post(f'{API}/ecos/{eco_id}/approve/', headers=headers)
if 'not the designated approver' in r.text.lower() or r.status_code == 403:
    p('Admin Bypass Failed! ' + r.text); sys.exit(1)
p('✅ Admin Bypass Fixed!')
