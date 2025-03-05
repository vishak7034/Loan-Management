# Loan Management System - Django REST API

## Overview
This Loan Management System is built using **Django REST Framework (DRF)**. It allows users to apply for loans, view repayment schedules, and foreclose loans early with interest adjustments. The system supports **role-based authentication**, JWT token authentication, and OTP-based email verification.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (Simple JWT), OTP via Nodemailer (SMTP)
- **Database**: PostgreSQL (Preferred) or MongoDB (Optional)
- **Deployment**: Render (Free Tier)

## Features
### **Authentication & Role-Based Access**
- User authentication using **JWT (Simple JWT)**.
- **Roles**: Admin & User.
- OTP email verification for new registrations.
- Every API request requires a valid JWT token.

### **Loan Management**
- Users can:
  - Apply for a loan with amount, tenure, and interest rate.
  - View their active and past loans.
  - View repayment schedules and total payable amount.
  - Foreclose loans before tenure completion (adjusted interest calculations apply).
- Admins can:
  - View all loans.
  - Manage user loan records.
  - Delete loan records.

### **Loan Calculation**
- **Yearly compound interest** with monthly installment calculations.
- Automatic calculation of total payable amount, interest, and monthly EMI.
- Early foreclosure allows users to settle loans with adjusted interest.

## Installation & Setup
### **Step 1: Clone Repository & Install Dependencies**
```sh
git clone https://github.com/vishak7034/Loan-Management/
cd loan_management
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **Step 2: Configure Database (PostgreSQL)**
Modify `settings.py`:
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='postgres://user:password@localhost:5432/loan_db')
}
```

### **Step 3: Run Migrations & Create Superuser**
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API Endpoints
### **Authentication**
✅ **Register**: `POST /api/register/`
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword"
}
```

✅ **Login**: `POST /api/login/`
```json
{
    "username": "testuser",
    "password": "testpassword"
}
```
_Response:_
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

### **Loan Management**
✅ **Create Loan**: `POST /api/loans/` (Include JWT token in headers)
```json
{
    "amount": 10000,
    "tenure": 12,
    "interest_rate": 10
}
```

✅ **Get Loan List**: `GET /api/loans/`
```sh
curl -X GET http://127.0.0.1:8000/api/loans/      -H "Authorization: Bearer your_access_token"
```

✅ **Foreclose Loan**: `POST /api/loans/{loan_id}/foreclose/`
```json
{
    "loan_id": "LOAN001"
}
```

## Deployment on Render
### **Step 1: Push to GitHub**
```sh
git init
git add .
git commit -m "Initial commit"
git remote add origin <your_repo_url>
git push -u origin main
```

### **Step 2: Set Up Render Web Service**
1. Go to [Render](https://render.com/).
2. Create a **New Web Service**.
3. Connect GitHub repo and select your project.
4. Set environment variables:
   ```sh
   DATABASE_URL=<your_postgresql_url>
   SECRET_KEY=<your_secret_key>
   DEBUG=False
   ```
5. Set **Start Command**:
   ```sh
   gunicorn loan_management.wsgi:application
   ```
6. Deploy 🚀

## Submission Guidelines
✅ **GitHub Repository** with source code, `README.md`, and `requirements.txt`.
✅ **Postman/Thunder Client Collection** for testing APIs.
✅ **Live API URL** on Render.
✅ **Documentation** for API endpoints and setup.

## Notes
- Follow **PEP 8** coding standards.
- Use proper error handling and response validation.
- Test API endpoints thoroughly.

**🚀 Happy Coding!**
