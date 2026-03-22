import requests, sys
API = 'http://127.0.0.1:8000/api'
def p(m): print(m)

# 1. Login as Admin to setup the stage and ECO
r = requests.post(f'{API}/auth/login/', json={'login_id':'admin01', 'password':'PLM@1234'})
token_admin = r.json()['access']
h_admin = {'Authorization': f'Bearer {token_admin}'}

# Get Approver01 user ID
users = requests.get(f'{API}/auth/users/', headers=h_admin).json()
app_user_id = next(u['id'] for u in users if u['login_id'] == 'approver01')

# Setup Stage config: Make Approver01 REQUIRED for 'In Review' (sequence=10)
stages = requests.get(f'{API}/settings/stages/', headers=h_admin).json()
in_review = next(s['id'] for s in stages if s['name'] == 'In Review')

# Delete existing configs for this stage for clean test
configs = requests.get(f'{API}/settings/approvals/', headers=h_admin).json()
for c in configs:
    if c['stage'] == in_review:
        requests.delete(f'{API}/settings/approvals/{c["id"]}/', headers=h_admin)

res = requests.post(f'{API}/settings/approvals/', json={'stage': in_review, 'user': app_user_id, 'category': 'required'}, headers=h_admin)
if res.status_code != 201:
    p("Failed to setup config: " + res.text)
    sys.exit(1)

# 2. Create and Start ECO
prods = requests.get(f'{API}/products/', headers=h_admin).json()
eco_data = {'title': 'Approver Test', 'eco_type': 'product', 'product': prods[0]['id']}
r = requests.post(f'{API}/ecos/', json=eco_data, headers=h_admin)
eco_id = r.json()['id']
requests.post(f'{API}/ecos/{eco_id}/start/', headers=h_admin) # Now at New
requests.patch(f'{API}/ecos/{eco_id}/stage/next/', headers=h_admin) # Now at In Review

# 3. Login as Approver
r = requests.post(f'{API}/auth/login/', json={'login_id':'approver01', 'password':'PLM@1234'})
h_app = {'Authorization': f'Bearer {r.json()["access"]}'}

# 4. Approver01 Approves
r = requests.post(f'{API}/ecos/{eco_id}/approve/', headers=h_app)
if r.status_code != 200:
    p('Approver could not approve: ' + r.text)
    sys.exit(1)

# 5. Check stage
eco = requests.get(f'{API}/ecos/{eco_id}/', headers=h_app).json()
if eco['stage_name'] == 'In Review':
    p('STAGE DID NOT ADVANCE!')
else:
    p(f'✅ Stage successfully advanced to {eco["stage_name"]}')
