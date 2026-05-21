"""
Script to create an admin user for Himalayan Pet Studio
Run this with: python create_admin.py
"""
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'himalayan_pet_studio.settings')


try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

django.setup()

from accounts.models import User

def create_admin():
    """Create admin user if not exists"""
    username = 'admin'
    email = 'admin@himalayan.com'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"Admin user '{username}' already exists!")
        admin = User.objects.get(username=username)
        admin.role = 'admin'
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        print(f"Updated role to 'admin' for user '{username}'")
    else:
        admin = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        print(f"Admin user created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")

if __name__ == '__main__':
    create_admin()
