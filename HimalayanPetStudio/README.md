# 🐾 Himalayan Pet Studio

A comprehensive pet grooming studio management system built with Django 4.2.7 and Bootstrap 5. This web application provides a complete solution for managing pet grooming appointments, products, customer reviews, and user accounts.

---

## 🚀 Quick Start (Easy Setup)

### Prerequisites
- Python 3.8 or higher
- MySQL Server (XAMPP or standalone)

### One-Click Installation

1. **Setup Dependencies** - Double-click `setup.bat`
   - Creates virtual environment automatically
   - Installs all required packages
   
2. **Start MySQL** - Open XAMPP Control Panel and start MySQL

3. **Run the Project** - Double-click `run.bat`
   - Server starts at: http://127.0.0.1:8000/

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 📋 Features

### 👤 User Management
- **User Registration & Authentication** - Secure signup and login system
- **Role-Based Access Control** - Separate dashboards for Admin and Customers
- **User Profile Management** - Upload profile pictures and update personal information
- **Admin User Management** - View and manage all registered users

### 📅 Appointment System
- **Online Booking** - Customers can book grooming appointments
- **Time Validation** - Working hours (9 AM - 6 PM) enforcement
- **Double Booking Prevention** - Prevents scheduling conflicts
- **Appointment Status Tracking** - Pending, Approved, Confirmed, Cancelled
- **Confirm Booking Feature** - Admin can approve and confirm appointments
- **Conditional Edit Access** - Users can only edit pending appointments
- **Clickable Appointment Rows** - View detailed information with pet owner details

### 🛍️ Product Management
- **Product Catalog** - Browse all available pet products
- **Search & Filter** - Search by name/description, filter by category
- **Sorting Options** - Sort by newest, price (low to high, high to low), highest rating
- **Pagination** - 10 products per page for better performance
- **Product Details** - View complete product information with images
- **Stock Management** - Real-time stock quantity tracking
- **Admin Product CRUD** - Add, edit, and delete products (Admin only)
- **Clickable Product Cards** - Direct navigation to product details

### 🛒 Shopping Cart
- **Add to Cart** - Add products with custom quantities
- **Cart Badge Counter** - Dynamic cart item count in navbar
- **Quantity Controls** - Increase/decrease product quantities in cart
- **Subtotal Calculation** - Automatic price calculation per item
- **Total Calculation** - Cart total with all items
- **Remove Items** - Delete individual products from cart
- **Clear Cart** - Remove all items at once

### ⭐ Rating & Review System
- **Product Reviews** - Customers can rate and review purchased products
- **5-Star Rating System** - Visual star rating with radio buttons
- **Purchase Verification** - Only purchasers can leave reviews
- **One Review Per Product** - Database constraint prevents duplicates
- **Review Management** - Edit and delete your own reviews
- **Average Rating Display** - Shows calculated average rating on products
- **Review Count** - Total number of reviews per product
- **Top Rated Products** - Displays products with 4+ stars on homepage

### 🏠 Home Page
- **Appointment Booking Form** - Quick access to book grooming services
- **Service Showcase** - Detailed service cards with pricing and features
  - Bath & Brush - Rs. 500
  - Haircut & Styling - Rs. 800
  - Full Grooming Package - Rs. 1500
- **Why Choose Us Section** - Highlights of studio benefits
- **Top Rated Products Carousel** - Horizontally scrollable product showcase
- **Top Selling Products** - Popular items carousel display

### 📧 Contact System
- **Contact Us Page** - Contact form for customer inquiries
- **Message Storage** - All messages saved in database
- **Unread Message Counter** - Badge notification for admin
- **Admin Message Management** - View and manage all contact messages

### 📊 Admin Dashboard
- **Statistics Overview** - Total users, appointments, products, messages
- **Revenue Tracking** - Total sales and revenue display
- **Recent Activity** - Latest appointments and orders
- **Quick Access Links** - Navigate to all management sections

### 🎨 User Interface
- **Responsive Design** - Mobile-friendly Bootstrap 5 layout
- **Modern UI/UX** - Purple gradient theme with smooth transitions
- **Hover Effects** - Interactive card animations
- **Loading States** - Visual feedback for user actions
- **Custom Scrollbars** - Styled scrollbars for horizontal sections
- **Font Awesome Icons** - Professional icon set throughout

---

## 🛠️ Technology Stack

### Backend
- **Django 4.2.7** - Python web framework
- **Python 3.13.9** - Programming language
- **MySQL** - Database (via PyMySQL)
- **Pillow** - Image processing for profile pictures and product images

### Frontend
- **Bootstrap 5.3.0** - CSS framework
- **Font Awesome 6** - Icon library
- **JavaScript** - Interactive features

---

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.13.9 or higher**
- **MySQL Server** (with root access)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd HimalayanPetStudio
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 5. Configure Database

Create a MySQL database:
```sql
CREATE DATABASE himalayan_pet_studio;
```

Update database settings in `backend/himalayan_pet_studio/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'himalayan_pet_studio',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

### 6. Run Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 8. Run Development Server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

---

## 🚀 Quick Start Guide

### Running the Project (After Initial Setup)

1. **Navigate to project directory:**
   ```bash
   cd HimalayanPetStudio
   ```

2. **Activate virtual environment:**
   
   **Windows (PowerShell/CMD):**
   ```bash
   .venv\Scripts\activate
   ```
   
   **Linux/Mac:**
   ```bash
   source .venv/bin/activate
   ```

3. **Navigate to backend folder:**
   ```bash
   cd backend
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

6. **Stop the server:**
   - Press `CTRL + C` in the terminal

### Common Commands

**Create database migrations:**
```bash
python manage.py makemigrations
```

**Apply migrations:**
```bash
python manage.py migrate
```

**Create admin user:**
```bash
python manage.py createsuperuser
```

**Collect static files:**
```bash
python manage.py collectstatic
```

**Run on different port:**
```bash
python manage.py runserver 8001
```

**Check for issues:**
```bash
python manage.py check
```

---

## 📁 Project Structure

```
HimalayanPetStudio/
│
├── backend/
│   ├── accounts/              # User authentication & profiles
│   │   ├── migrations/
│   │   ├── models.py          # User model with profile picture
│   │   ├── views.py           # Authentication views
│   │   └── forms.py           # User forms
│   │
│   ├── appointments/          # Appointment management
│   │   ├── migrations/
│   │   ├── models.py          # Appointment model
│   │   ├── views.py           # Booking & management views
│   │   └── forms.py           # Appointment forms
│   │
│   ├── products/              # Product & cart management
│   │   ├── migrations/
│   │   ├── models.py          # Product, Category, Cart, Sale, Review
│   │   ├── views.py           # Product CRUD & cart operations
│   │   └── forms.py           # Product & review forms
│   │
│   ├── himalayan_pet_studio/  # Project settings
│   │   ├── settings.py        # Configuration
│   │   ├── urls.py            # URL routing
│   │   └── wsgi.py            # WSGI config
│   │
│   ├── media/                 # Uploaded files
│   │   ├── products/          # Product images
│   │   └── profile_pictures/  # User profile pictures
│   │
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Custom styles
│   │   └── js/
│   │       └── main.js        # JavaScript functions
│   │
│   └── templates/
│       ├── base.html          # Base template
│       ├── admin_base.html    # Admin base template
│       ├── home.html          # Homepage
│       │
│       ├── accounts/          # User templates
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── user_profile.html
│       │   └── contact_us.html
│       │
│       ├── appointments/      # Appointment templates
│       │   ├── appointment_form.html
│       │   ├── appointment_list.html
│       │   └── appointment_detail.html
│       │
│       └── products/          # Product templates
│           ├── product_list.html
│           ├── product_detail.html
│           ├── cart.html
│           └── review_form.html
│
├── .venv/                     # Virtual environment (created)
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

---

## 👥 User Roles & Access

### Customer Features
- Register and login
- Book appointments
- Browse and purchase products
- Add products to cart
- Leave product reviews (after purchase)
- View and edit profile
- Track appointment status

### Admin Features
- All customer features
- Manage users
- Approve/confirm appointments
- Add/edit/delete products
- Manage product categories
- View all contact messages
- Access sales reports
- View dashboard statistics

---



---

## 📝 Usage Guide

### For Customers:

1. **Register**: Create an account at `/accounts/register/`
2. **Login**: Sign in at `/accounts/login/`
3. **Book Appointment**: Fill the form on homepage or `/appointments/`
4. **Browse Products**: Visit `/products/` to see available items
5. **Add to Cart**: Click "Add to Cart" on product pages
6. **Purchase Products**: Complete checkout process
7. **Leave Reviews**: Rate products you've purchased
8. **Manage Profile**: Update your details at `/profile/`

### For Admins:

1. **Access Dashboard**: Login redirects to `/admin-dashboard/`
2. **Manage Appointments**: View and approve at `/appointments/`
3. **Manage Products**: Add/edit products at `/products/`
4. **View Users**: Access user list at `/users/`
5. **Check Messages**: View inquiries at `/contact-messages/`
6. **View Reports**: Access sales data at `/reports/`

---

## 🎨 Key URLs

| Page | URL | Access |
|------|-----|--------|
| Homepage | `/` | Public |
| Login | `/accounts/login/` | Public |
| Register | `/accounts/register/` | Public |
| Profile | `/profile/` | Authenticated |
| Products | `/products/` | Public |
| Product Detail | `/products/<id>/` | Public |
| Cart | `/products/cart/` | Authenticated |
| Appointments | `/appointments/` | Authenticated |
| Contact Us | `/contact/` | Public |
| Admin Dashboard | `/admin-dashboard/` | Admin Only |
| User Management | `/users/` | Admin Only |
| Reports | `/reports/` | Admin Only |

---

## 📦 Dependencies

Main Python packages (see `requirements.txt` for complete list):

```
Django==4.2.7
PyMySQL==1.1.0
Pillow==10.1.0
```