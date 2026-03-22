# PLM System — Roles & Permissions

> ✅ = Allowed &nbsp;&nbsp; ❌ = Not Allowed &nbsp;&nbsp; ⚠️ = Only if designated in ApprovalConfig

| Feature / Action | Admin | Engineering | Approver | Operations |
| :--- | :---: | :---: | :---: | :---: |
| **LOGIN & DASHBOARD** | | | | |
| Login to system | ✅ | ✅ | ✅ | ✅ |
| View Dashboard | ✅ | ✅ | ✅ | ✅ |
| **USER MANAGEMENT** | | | | |
| Create / Edit / Delete Users | ✅ | ❌ | ❌ | ❌ |
| Assign User Roles | ✅ | ❌ | ❌ | ❌ |
| **PRODUCTS** | | | | |
| View Products | ✅ | ✅ | ✅ | ✅ |
| Create Product | ✅ | ✅ | ❌ | ❌ |
| Edit Product | ✅ | ✅ | ❌ | ❌ |
| Delete Product | ✅ | ✅ | ❌ | ❌ |
| **BILL OF MATERIALS (BOM)** | | | | |
| View BOMs | ✅ | ✅ | ✅ | ✅ |
| Create BOM | ✅ | ✅ | ❌ | ❌ |
| Edit BOM | ✅ | ✅ | ❌ | ❌ |
| Delete BOM | ✅ | ✅ | ❌ | ❌ |
| **ENGINEERING CHANGE ORDERS (ECO)** | | | | |
| View ECOs | ✅ | ✅ | ✅ | ✅ |
| Create ECO | ✅ | ✅ | ❌ | ❌ |
| Edit ECO (draft only) | ✅ | ✅ | ❌ | ❌ |
| Start ECO Workflow | ✅ | ✅ | ❌ | ❌ |
| Validate / Advance Stage | ✅ | ✅ (own ECOs) | ❌ | ❌ |
| Approve ECO at a Stage | ✅ | ⚠️ | ⚠️ | ❌ |
| Reject ECO | ✅ | ❌ | ✅ | ❌ |
| Propose Changes (Open BOM/Product) | ✅ | ✅ | ❌ | ❌ |
| **SETTINGS** | | | | |
| Manage ECO Stages | ✅ | ❌ | ❌ | ❌ |
| Manage Work Centers | ✅ | ❌ | ❌ | ❌ |
| Configure Approval Rules | ✅ | ❌ | ❌ | ❌ |
| **REPORTS & AUDIT** | | | | |
| View Reports & Analytics | ✅ | ✅ | ✅ | ✅ |
| View Audit Logs | ✅ | ❌ | ❌ | ❌ |
