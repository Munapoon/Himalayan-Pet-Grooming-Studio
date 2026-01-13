# Setup Instructions for Himalayan Pet Studio

## Quick Setup Guide

### 1. Create MySQL Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE himalayan_pet_studio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Configure Database Settings

Open `backend/himalayan_pet_studio/settings.py` and update line 80-90 with your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'himalayan_pet_studio',
        'USER': 'root'
        'PASSWORD': '', 
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Install Required Packages

Open Command Prompt (cmd) and navigate to the backend directory:

```bash
cd c:\Users\bisha\OneDrive\Desktop\HimalayanPetStudio\backend
pip install -r requirements.txt
```

If you encounter issues installing mysqlclient, you may need to:
- Install Visual C++ Build Tools
- Or install a pre-built wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

### 4. Create Database Tables

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```
```

### 7. Run the Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Login**: http://127.0.0.1:8000/accounts/login/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **Register**: http://127.0.0.1:8000/accounts/register/

### 9. Test the Application

1. **As Admin**:
   - Login with admin credentials
   - You'll be redirected to Admin Dashboard
   - View statistics and manage appointments

2. **As User**:
   - Register a new account (or create via Django admin)
   - Login with user credentials
   - Book appointments
   - Manage your appointments

## Troubleshooting

### Error: No module named 'MySQLdb'

Install mysqlclient:
```bash
pip install mysqlclient
```

### Error: Access denied for user

Check your MySQL username and password in `settings.py`

### Error: Unknown database

Create the database:
```sql
CREATE DATABASE himalayan_pet_studio;
```

### Port 8000 already in use

Use a different port:
```bash
python manage.py runserver 8080
```

## Features to Test

1. **User Registration**: Register a new user account
2. **User Login**: Login with different roles
3. **Book Appointment**: Create a new grooming appointment
4. **View Appointments**: See your bookings
5. **Update Appointment**: Edit appointment details
6. **Delete Appointment**: Remove an appointment
7. **Admin Dashboard**: View statistics (admin only)
8. **Status Management**: Change appointment status (admin only)

## Sample Data

You can create sample appointments to test the system:
1. Login as a regular user
2. Book appointments with different services
3. Login as admin to manage them

## Default Services Available

- Bath & Brush
- Haircut & Styling
- Nail Trimming
- Full Grooming Package
- Spa Treatment

## Support

If you encounter any issues:
1. Check that MySQL is running
2. Verify database credentials
3. Ensure all migrations are applied
4. Check the console for error messages
5. Review the `README.md` for detailed documentation
