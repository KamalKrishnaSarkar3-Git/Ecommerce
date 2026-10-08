<div align="center">

# 🌾 FarmDirect

### Connecting Farmers Directly with Consumers — Zero Middlemen

[![Live Demo](https://img.shields.io/badge/Demo-Live_Platform-brightgreen?style=for-the-badge&logo=googlechrome&logoColor=white)](https://yourdomain.com)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=1000&color=2E7D32&center=true&vcenter=true&width=650&lines=Farm-Fresh+Produce+Direct+to+Your+Doorstep;Empowering+Local+Indian+Agricultural+Communities;Built+with+Django+4.2+%2B+Bootstrap+5" alt="Typing SVG" />
</p>

</div>

---

## 🌐 Live Production Deployment

Access the live platform and check system statuses directly through the links below:

| Resource | Status | URL |
| :--- | :--- | :--- |
| **Live Web App** | ![Active](https://img.shields.io/badge/Status-Online-success?style=flat-square) | **[https://ecommerce-production-ed7b.up.railway.app](https://ecommerce-production-ed7b.up.railway.app)** |
| **Admin Portal** | ![Active](https://img.shields.io/badge/Auth-Restricted-orange?style=flat-square) | **[https://ecommerce-production-ed7b.up.railway.app/admin](https://ecommerce-production-ed7b.up.railway.app/admin)** |

> **Production Note:** Hosted with Gunicorn reverse-proxied through Nginx, featuring automated SSL certification via Let's Encrypt.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Quick Start Guide](#-quick-start-guide)
- [Demo Authentication](#-demo-authentication)
- [URL Directory](#-url-directory)
- [Database Configuration](#-database-configuration)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 📖 Overview

**FarmDirect** is a multi-sided e-commerce marketplace engineered to bridge the supply gap between agricultural producers and end retail customers. By digitizing inventory, cataloging organic certification, and providing local farm dashboards, FarmDirect cuts supply-chain overhead and passes the savings directly to farmers and households.

---

## ✨ Key Features

### 👨‍🌾 Farmer Operations (Sellers)
- **Storefront Setup:** Complete farm onboarding with bio, regional location, and certifications.
- **Produce Management:** Dynamic inventory creation with image uploads, MRP/discount settings, unit sizing, and harvest date logging.
- **Seller Metrics:** Real-time revenue analytics, pending shipments, and unit distribution charts.

### 🛒 Customer Experience (Buyers)
- **Curated Catalog:** Multi-facet filtering by category (fruits, vegetables, dairy, grains) and certified organic status.
- **Cart & Order Flow:** Live cart counter, checkout pipeline with delivery scheduling, and multi-option demo gateways (COD, UPI, Card).
- **Post-Purchase Engagement:** Historical order tracking and star ratings with verified-buyer product reviews.

### ⚙️ Platform Administration
- **Granular Control:** Complete Django admin dashboard for handling catalog taxonomies, user roles, and order overrides.
- **Data Integrity:** Inline order management and automated customer cart cleanups.

---

## 🧰 Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Core Backend** | Python 3.10+, Django 4.2 (MVT Architecture) |
| **Frontend & UI** | HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons |
| **Forms & Presentation** | django-crispy-forms, crispy-bootstrap5 |
| **Media Processing** | Pillow (PIL fork) |
| **Data Layer** | SQLite3 (Development) / MySQL 8.0+ (Production) |

---

## 📁 Project Architecture

```plaintext
ecommerce/
├── manage.py
├── requirements.txt
├── README.md
│
├── ecommerce/                   # Project Configuration
│   ├── settings.py              # Central runtime settings
│   ├── urls.py                  # Primary routing table
│   └── wsgi.py                  # WSGI web server hook
│
├── marketplace/                 # Main Application Module
│   ├── admin.py                 # Admin registration hooks
│   ├── forms.py                 # Django forms (Auth, Checkout, Products)
│   ├── models.py                # Database entity schemas
│   ├── views.py                 # Core request/response business logic
│   ├── urls.py                  # App-level URL routes
│   │
│   ├── management/commands/
│   │   └── seed_demo.py         # Automated database mock data generator
│   │
│   └── templates/marketplace/   # Presentation templates
│       ├── base.html            # Universal boilerplate (Navbar/Footer)
│       ├── home.html            # Platform homepage
│       ├── product_list.html    # Product shop & search filters
│       ├── cart.html            # Shopping cart
│       └── seller_dashboard.html# Farmer metrics & controls
│
└── static/                      # Static assets (Custom CSS & JS)



🚀 Quick Start Guide
1. Clone & Set Up Virtual Environment
Bash
# Clone the repository
git clone [https://github.com/your-username/farmdirect.git](https://github.com/your-username/farmdirect.git)
cd farmdirect

# Create virtual environment
python -m venv .venv

# Activate environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate


2. Install Dependencies
Bash
pip install -r requirements.txt


3. Database Migration
Bash
python manage.py makemigrations
python manage.py migrate


4. Seed Mock Data
Run the integrated seeding script to generate categories, farmer profiles, products, reviews, and test accounts:

Bash
python manage.py seed_demo --fresh


5. Launch the Local Server
Bash
python manage.py runserver
Navigate to http://127.0.0.1:8000/ in your browser.



🔑 Demo Authentication
Role	Username	Password	Access Area
Super Admin	admin	admin123	/admin/
Farmer (Seller)	ramesh_patel	farmer123	/seller/dashboard/
Customer (Buyer)	priya_sharma	customer123	/products/ & /cart/



🌐 URL Directory
Route	HTTP Method	Handler	Description
/	GET	home	Landing page
/products/	GET	product_list	Filterable product directory
/product/<slug>/	GET	product_detail	Product specifications & reviews
/cart/	GET	cart_view	User shopping basket
/checkout/	GET, POST	checkout	Address collection & checkout
/seller/dashboard/	GET	seller_dashboard	Farmer management hub
/seller/product/add/	GET, POST	add_product	Product listing portal
/admin/	GET, POST	Django Admin	Site-wide administrative backoffice



🐬 Database Configuration
1. Install Driver
Bash
pip install mysqlclient
# Alternatively, if building wheels fails on Windows:
# pip install pymysql


2. Configure Database in ecommerce/settings.py
Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'farmdirect_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


3. Initialize Schema
Bash
python manage.py migrate
python manage.py seed_demo --fresh



🐛 Troubleshooting
Unknown command: 'seed_demo'

Ensure an empty __init__.py exists inside both marketplace/management/ and marketplace/management/commands/.

ModuleNotFoundError: No module named 'PIL'

Pillow is required for product image handling:


Bash
pip install Pillow
PowerShell Execution Policy Error (PSSecurityException)

Allow scripts for the current user:


PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Broken Demo Images (Unsplash 503)

Replace the Unsplash query URL inside seed_demo.py with the Picsum mock generator:

Python
'image_url': f"[https://picsum.photos/seed/](https://picsum.photos/seed/){name.replace(' ', '')}/400/400"


📄 License
Distributed under the MIT License. See LICENSE for further details.


<FollowUp label="Want to create an automated Docker Compose setup for this Django and MySQL configuration?" query="Provide a production-ready Dockerfile and docker-compose.yml configuration to run this Django application alongside MySQL and Nginx."/>
