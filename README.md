# PLM Eco System

PLM Eco System is a Product Lifecycle Management application with a Django REST backend and a static frontend for managing products, BOMs, ECO workflows, approvals, audit history, and reports.

 video link:https://drive.google.com/file/d/1VJl7K2QCuy8wfdaDemwQsCxmTAVOrq8i/view?usp=sharing
 
## Features

- JWT-based authentication
- role-based access control
- product management
- BOM management
- ECO creation and approval flow
- configurable ECO stages and approvals
- audit logs
- reporting pages

## Tech Stack

- Backend: Django, Django REST Framework, SimpleJWT
- Database: PostgreSQL
- Frontend: HTML, CSS, Bootstrap, vanilla JavaScript

## Project Structure

```text
plm-eco-system/
├── backend/
│   ├── apps/
│   │   ├── approvals/
│   │   ├── audit/
│   │   ├── bom/
│   │   ├── eco/
│   │   ├── products/
│   │   ├── reports/
│   │   ├── settings_app/
│   │   └── users/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── pages/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── index.html
└── run.bat
```

## Requirements

- Python 3.12 recommended
- PostgreSQL

Backend Python packages:

- Django
- djangorestframework
- djangorestframework-simplejwt
- psycopg2-binary
- django-cors-headers
- Pillow
- python-decouple

## Environment Setup

Create `backend/.env` with your local database values.

Example:

```env
SECRET_KEY=django-insecure-plm-hackathon-secret-change-in-prod
DEBUG=True
ALLOWED_HOSTS=*

DB_NAME=plm_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## Installation

### 1. Create virtual environment

```powershell
cd backend
python -m venv env
.\env\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run migrations

```powershell
python manage.py migrate
```

### 4. Optional seed data

```powershell
python manage.py seed
```

## Running the Project

### Option 1: Use the batch file

From the project root:

```powershell
.\run.bat
```

This starts:

- backend: `http://127.0.0.1:8000`
- frontend: `http://127.0.0.1:8080`

### Option 2: Run manually

Backend:

```powershell
cd backend
.\env\Scripts\activate
python manage.py runserver
```

Frontend:

```powershell
cd frontend
python -m http.server 8080
```

## Main Modules

- `users`: authentication, roles, user APIs
- `products`: products and attachments
- `bom`: BOM records, operations, and components
- `eco`: engineering change orders and proposed changes
- `approvals`: stage approval configuration and approval records
- `settings_app`: ECO stage setup and system settings
- `audit`: audit event tracking
- `reports`: reporting endpoints and pages

## API Base URL

The frontend is configured to call the backend at:

```text
http://localhost:8000/api
```

## Notes

- The backend uses PostgreSQL, not SQLite.
- Media uploads are stored inside `backend/media/`.
- The frontend is a static site served separately from Django.
- Open the frontend through the local server, not by opening HTML files directly.

## Troubleshooting

### Backend does not start

Check:

- virtual environment is activated
- requirements are installed
- PostgreSQL is running
- `backend/.env` has valid DB credentials

### Frontend loads but API fails

Check:

- Django server is running on port `8000`
- frontend server is running on port `8080`
- browser console for failed requests

### Static pages look broken

Run the frontend with:

```powershell
cd frontend
python -m http.server 8080
```

and then open:

```text
http://127.0.0.1:8080
```
