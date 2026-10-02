markdown
# 🌾 FarmDirect — Farmer-to-Consumer E-Commerce Platform

A full-stack Django e-commerce platform that connects **farmers directly with consumers**, eliminating middlemen. Farmers can list fresh produce; customers can browse, add to cart, checkout, and leave reviews.

Built with **Django 4.2 + Bootstrap 5 + SQLite** — ready to run on any PC/laptop in minutes.

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Prerequisites](#-prerequisites)
5. [Installation (Step-by-Step)](#-installation-step-by-step)
6. [Database Migration](#-database-migration)
7. [Loading Demo Data](#-loading-demo-data)
8. [Running the Server](#-running-the-server)
9. [Demo Login Credentials](#-demo-login-credentials)
10. [How to Use](#-how-to-use)
11. [URL Reference](#-url-reference)
12. [Troubleshooting](#-troubleshooting)
13. [Switching to MySQL (Optional)](#-switching-to-mysql-optional)
14. [License](#-license)

---

## ✨ Features

### 👨‍🌾 For Farmers (Sellers)
- Register and create a farm profile
- Add / edit / delete products with images
- Set price, MRP, unit, stock, harvest date
- Mark products as organic or featured
- View seller dashboard with sales stats
- See orders for their products

### 🛒 For Customers (Buyers)
- Browse products by category
- Search products by name or description
- Filter by organic / category
- Add to cart, update quantity, remove items
- Checkout with delivery details
- Multiple payment methods (COD, UPI, Card — demo only)
- View order history and track status
- Write reviews with 1–5 star ratings

### ⚙️ Admin
- Full Django admin panel
- Manage categories, farmers, products, orders, reviews
- Inline order items editing
- Revenue & status tracking

### 🎨 UI / UX
- Fully responsive (mobile / tablet / desktop)
- Bootstrap 5 + Bootstrap Icons
- Product cards with discount badges
- Star-rating display
- Flash messages for actions
- Category dropdown in navbar
- Live cart item count

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Django 4.2 |
| **Database** | SQLite (dev) / MySQL (production-ready config included) |
| **Frontend** | HTML5, Bootstrap 5.3, Bootstrap Icons |
| **Forms** | django-crispy-forms + crispy-bootstrap5 |
| **Images** | Pillow |
| **Auth** | Django built-in authentication |

---

## 📁 Project Structure
ecommerce/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
│
├── ecommerce/ # Project config
│ ├── init.py
│ ├── settings.py # DB, apps, templates config
│ ├── urls.py # Root URL routing
│ ├── wsgi.py
│ └── asgi.py
│
├── marketplace/ # Main app
│ ├── init.py
│ ├── admin.py # Admin panel registrations
│ ├── apps.py
│ ├── context_processors.py # Cart count in navbar
│ ├── forms.py # Signup, Product, Review, Checkout
│ ├── models.py # Category, Product, Order, Review...
│ ├── urls.py # App URL routing
│ ├── views.py # All business logic
│ │
│ ├── migrations/
│ │ └── 0001_initial.py
│ │
│ ├── management/
│ │ ├── init.py
│ │ └── commands/
│ │ ├── init.py
│ │ └── seed_demo.py # ⭐ Demo data seeder
│ │
│ └── templates/marketplace/
│ ├── base.html # Layout with navbar + footer
│ ├── home.html # Landing page
│ ├── product_list.html # Shop with filters
│ ├── product_detail.html # Product + reviews
│ ├── cart.html # Shopping cart
│ ├── checkout.html # Order form
│ ├── order_success.html
│ ├── my_orders.html
│ ├── seller_dashboard.html # Farmer panel
│ ├── product_form.html # Add/Edit product
│ ├── signup.html
│ ├── _product_card.html # Reusable card
│ └── registration/
│ └── login.html
│
├── static/
│ ├── css/style.css
│ └── js/main.js
│
├── templates/registration/ # (fallback login templates)
│
└── media/ # Uploaded product images
└── products/

text

---

## ✅ Prerequisites

Before you start, make sure you have:

| Requirement | Version | Check Command |
|---|---|---|
| **Python** | 3.10 or higher | `python --version` |
| **pip** | Latest | `pip --version` |
| **Git** (optional) | Any | `git --version` |
| **Code Editor** | VS Code / PyCharm | — |

> ⚠️ **Windows users:** Make sure Python is added to PATH. If `python` doesn't work, try `py` instead.

---

## 🚀 Installation (Step-by-Step)

### Step 1 — Open terminal in the project folder

```bash
cd "path\to\ecommerce"
Example on Windows:

powershell
cd "C:\Users\USER\Desktop\WARNING\Language\Django\ecommerce site\ecommerce"
Step 2 — Create a virtual environment
bash
python -m venv .venv
Step 3 — Activate the virtual environment
Windows (PowerShell):

powershell
.venv\Scripts\Activate.ps1
Windows (CMD):

cmd
.venv\Scripts\activate.bat
macOS / Linux:

bash
source .venv/bin/activate
You should see (.venv) at the start of your prompt:

text
(.venv) PS C:\...\ecommerce>
If PowerShell blocks activation, run once:

powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Step 4 — Install dependencies



Create requirements.txt (if it doesn't exist):
txt
Django==4.2.7
Pillow==10.1.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7
Then install:

bash
pip install -r requirements.txt
Or install individually:

bash
pip install Django==4.2.7 Pillow django-crispy-forms crispy-bootstrap5
Step 5 — Verify installation
bash
python -c "import django; print(django.get_version())"
Should output: 4.2.7

🗄️ Database Migration
Django uses migrations to create DB tables. Run:

bash
# 1. Create migration files from models
python manage.py makemigrations

# 2. Apply migrations to the database
python manage.py migrate
Expected output:

text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, marketplace, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying marketplace.0001_initial... OK
What just happened:

A db.sqlite3 file was created in your project root

All tables for Category, FarmerProfile, Product, Cart, CartItem, Order, OrderItem, Review were created

💡 Re-running migrate is safe — Django skips already-applied migrations.

🌱 Loading Demo Data
The project ships with a demo seeder that populates realistic Indian farm data.

Option A — Full fresh seed (recommended for first run)
bash
python manage.py seed_demo --fresh
This will:

🗑️ Wipe existing demo data

✅ Create 8 categories

✅ Create 6 farmers (Nashik, Anand, Wayanad, Ludhiana, Ratnagiri, Coorg)

✅ Create 5 customers

✅ Create 47 products (vegetables, fruits, dairy, grains, spices, honey, organic, flowers)

✅ Create ~150 product reviews

✅ Create 3 pre-filled carts

✅ Create ~20 historical orders with varied statuses

✅ Create admin superuser

Option B — Add without wiping
bash
python manage.py seed_demo
Option C — Custom random seed (for reproducibility)
bash
python manage.py seed_demo --fresh --seed 123
Expected output
text
Wiping existing demo data...
Creating categories...
Creating farmers...
Creating customers...
Creating products...
Creating reviews...
Creating carts...
Creating order history...
Superuser created: admin / admin123

============================================================
✅ DEMO DATA SEEDED SUCCESSFULLY
============================================================
  Categories : 8
  Farmers    : 6
  Products   : 47
  Customers  : 5
  Reviews    : 152
  Carts      : 3
  Orders     : 21
  OrderItems : 63
============================================================

🔑 LOGIN CREDENTIALS
  Admin    : admin / admin123
  Farmer   : ramesh_patel / farmer123
  Customer : priya_sharma / customer123
============================================================
▶️ Running the Server
bash
python manage.py runserver
Expected output:

text
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 4.2.7, using settings 'ecommerce.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
Open in your browser
URL	Page
http://127.0.0.1:8000/	🏠 Homepage
http://127.0.0.1:8000/products/	🛍️ All products
http://127.0.0.1:8000/accounts/login/	🔐 Login
http://127.0.0.1:8000/signup/	📝 Sign up
http://127.0.0.1:8000/admin/	⚙️ Admin panel
Stop the server
Press CTRL + C in the terminal.

Run on a different port
bash
python manage.py runserver 8080
Make it accessible on your local network
bash
python manage.py runserver 0.0.0.0:8000
Then access via http://YOUR_LOCAL_IP:8000/ from another device on the same Wi-Fi.

🔑 Demo Login Credentials
👑 Admin (Django admin panel)
Username	Password
admin	admin123
👨‍🌾 Farmers (all share the same password)
Username	Password	Farm
ramesh_patel	farmer123	Ramesh Organic Farm
sunita_devi	farmer123	Sunita Dairy & Greens
krishnan_m	farmer123	Krishnan Hill Farms
gurpreet_singh	farmer123	Punjab Wheat Co.
laxmi_reddy	farmer123	Laxmi Fruit Orchards
bhaskar_rao	farmer123	Bhaskar Honey Apiary
🛒 Customers (all share the same password)
Username	Password	Cart Pre-filled?
priya_sharma	customer123	✅
arjun_mehta	customer123	✅
neha_verma	customer123	✅
vikram_joshi	customer123	—
ananya_iyer	customer123	—
🎯 How to Use
🧑‍💼 I want to buy products (Customer)
Login as priya_sharma / customer123

Browse products on /products/

Click any product → "Add to Cart"

Go to /cart/ → review items → "Proceed to Checkout"

Fill delivery details → "Place Order"

View order in /my-orders/

Leave a review on the product page

👨‍🌾 I want to sell products (Farmer)
Login as ramesh_patel / farmer123

Go to /seller/dashboard/

Click "+ Add Product"

Fill the form (category, name, price, stock, image)

Save → product appears on the shop immediately

View orders for your products in the dashboard

⚙️ I want to manage everything (Admin)
Login at /admin/ with admin / admin123

Manage: Categories, Products, Orders, Reviews, Farmers

Edit orders inline (add/remove items, change status)

Bulk operations supported

🌐 URL Reference
URL	Method	View	Purpose
/	GET	home	Landing page
/products/	GET	product_list	Shop + search + filter
/product/<slug>/	GET	product_detail	Product + reviews
/product/<slug>/review/	POST	add_review	Submit review
/signup/	GET/POST	signup	Register
/accounts/login/	GET/POST	Django auth	Login
/accounts/logout/	POST	Django auth	Logout
/cart/	GET	cart_view	View cart
/cart/add/<id>/	GET	add_to_cart	Add item
/cart/update/<id>/	POST	update_cart	Change qty
/cart/remove/<id>/	GET	remove_from_cart	Delete item
/checkout/	GET/POST	checkout	Place order
/order/success/<id>/	GET	order_success	Confirmation
/my-orders/	GET	my_orders	Order history
/seller/dashboard/	GET	seller_dashboard	Farmer panel
/seller/product/add/	GET/POST	add_product	New product
/seller/product/<id>/edit/	GET/POST	edit_product	Edit product
/seller/product/<id>/delete/	POST	delete_product	Delete product
/admin/	GET	Django admin	Superuser panel
🐛 Troubleshooting
❌ python: command not found
Fix (Windows): Use py instead of python:

powershell
py -m venv .venv
py manage.py runserver
Or add Python to PATH during installation.

❌ No module named django
Cause: Virtual env not activated or Django not installed.

bash
# Make sure (.venv) appears in prompt
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
❌ ModuleNotFoundError: No module named 'PIL'
Fix:

bash
pip install Pillow
❌ Unknown command: 'seed_demo'
Cause: Missing __init__.py files.

Ensure these exist (even if empty):

text
marketplace/management/__init__.py
marketplace/management/commands/__init__.py
Create with:

powershell
New-Item -ItemType File -Force marketplace\management\__init__.py
New-Item -ItemType File -Force marketplace\management\commands\__init__.py
❌ KeyError: 'dairy' during seeding
Cause: Category slug mismatch (Dairy & Eggs → dairy-eggs).

Fix: Add explicit slug key to each entry in CATEGORIES inside seed_demo.py and use cat_map[c['slug']] = cat. See [docs/fix-category-slug.md] if included.

❌ no such table: marketplace_category
Fix:

bash
python manage.py migrate
❌ Port 8000 is already in use
Fix:

bash
python manage.py runserver 8001
❌ Please enter a correct username and password
Fix: Re-run the seeder (it may have rolled back):

bash
python manage.py seed_demo --fresh
Or reset a specific user's password:

bash
python manage.py changepassword priya_sharma
❌ Images not showing
Cause: source.unsplash.com deprecated (returns 503).

Fix: In seed_demo.py, replace:

python
'image_url': f"https://source.unsplash.com/400x400/?{name.replace(' ', ',').lower()}",
with:

python
'image_url': f"https://picsum.photos/seed/{name.replace(' ', '')}/400/400",
Then re-run python manage.py seed_demo --fresh.

❌ CSRF verification failed
Fix: Make sure {% csrf_token %} is present in every POST form. It already is in the provided templates.

❌ DisallowedHost at /
Fix: Add your IP/hostname to ALLOWED_HOSTS in ecommerce/settings.py:

python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'your-ip']
❌ PowerShell execution policy error
Fix (run once):

powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
🐬 Switching to MySQL (Optional)
The project is SQLite by default. To use MySQL:

1. Install MySQL client
bash
pip install mysqlclient
On Windows, if mysqlclient fails, download the wheel from PyPI mysqlclient wheels or use pymysql:

bash
pip install pymysql
Then add to ecommerce/__init__.py:

python
import pymysql
pymysql.install_as_MySQLdb()
2. Create database
sql
CREATE DATABASE farmdirect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
3. Update ecommerce/settings.py
Comment out the SQLite config and uncomment the MySQL block:

python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'farmdirect_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
4. Migrate & seed
bash
python manage.py migrate
python manage.py seed_demo --fresh
🧪 Quick Sanity Check
Run these commands after setup to verify everything works:

bash
# 1. Django check (no errors)
python manage.py check

# 2. Show migrations status
python manage.py showmigrations

# 3. Count objects in DB
python manage.py shell -c "from marketplace.models import *; print('Products:', Product.objects.count(), '| Orders:', Order.objects.count(), '| Users:', __import__('django.contrib.auth.models', fromlist=['User']).User.objects.count())"

# 4. Run tests (if any)
python manage.py test
Expected output for step 3:

text
Products: 47 | Orders: 21 | Users: 12
📊 Database Schema (High Level)
text
User (Django built-in)
 ├── FarmerProfile (1:1)  → farm_name, location, bio, rating
 ├── Cart (1:1)           → CartItem (M:1) → Product
 ├── Order (1:N)          → OrderItem (M:1) → Product
 └── Review (1:N)         → Product

Category (1:N) → Product
Product (N:1)  → User (farmer)
Product (1:N)  → Review
📦 requirements.txt
txt
Django==4.2.7
Pillow==10.1.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7
🚢 Production Deployment (Bonus)
For a real deployment (not localhost), you'd additionally need:

bash
pip install gunicorn whitenoise psycopg2-binary
DEBUG = False in settings

Set a strong SECRET_KEY (use environment variables)

Configure ALLOWED_HOSTS

Use PostgreSQL or MySQL

Serve static files via WhiteNoise or Nginx

Run with Gunicorn behind Nginx

Enable HTTPS

Use S3 / Cloudinary for media storage

Add Razorpay / Stripe for real payments

🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature/your-feature

Commit: git commit -m "Add feature"

Push: git push origin feature/your-feature

Open a Pull Request

📄 License
This project is released under the MIT License — free to use, modify, and distribute.

🙏 Acknowledgements
Django — web framework

Bootstrap 5 — UI framework

Bootstrap Icons — icon set

Indian farming community 🌾 — for inspiration

Made with ❤️ for farmers and consumers.

Happy farming! 🌱

text

---

## 📝 Also Create `requirements.txt`

In your project root, create `requirements.txt` with:

```txt
Django==4.2.7
Pillow==10.1.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7
📌 What This README Covers
Section	Purpose
Features	Shows anyone what the project does
Tech Stack	Quick tech overview
Project Structure	Visual tree so people find files fast
Prerequisites	What to install before starting
Installation	Copy-paste commands from zero
Migration	How to create DB tables
Demo Data	One-command seeding
Running Server	How to launch
Login Credentials	All usernames & passwords
How to Use	Role-based walkthrough
URL Reference	Every route in one table
Troubleshooting	The 12 most common errors you've already hit
MySQL switch	Production DB setup
Sanity Check	Verify installation in 10 seconds
