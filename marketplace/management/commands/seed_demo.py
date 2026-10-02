"""
Django management command to seed the database with realistic demo data.
Run: python manage.py seed_demo
Wipe & reseed: python manage.py seed_demo --fresh
"""
import random
from datetime import timedelta, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from marketplace.models import (
    Category, FarmerProfile, Product, Review, Cart, CartItem,
    Order, OrderItem
)


CATEGORIES = [
    {"name": "Vegetables", "slug": "vegetables", "icon": "flower1",
     "description": "Fresh farm-grown vegetables"},
    {"name": "Fruits", "slug": "fruits", "icon": "apple",
     "description": "Seasonal & exotic fruits"},
    {"name": "Dairy & Eggs", "slug": "dairy", "icon": "egg-fried",
     "description": "Milk, paneer, eggs & more"},
    {"name": "Grains & Pulses", "slug": "grains", "icon": "basket",
     "description": "Rice, wheat, dal, millets"},
    {"name": "Spices & Herbs", "slug": "spices", "icon": "flower2",
     "description": "Whole & ground spices"},
    {"name": "Honey & Preserves", "slug": "honey", "icon": "droplet",
     "description": "Raw honey, jams, pickles"},
    {"name": "Organic Specials", "slug": "organic", "icon": "leaf",
     "description": "Certified organic produce"},
    {"name": "Flowers & Plants", "slug": "flowers", "icon": "flower3",
     "description": "Fresh flowers and saplings"},
]

FARMERS = [
    {"username": "ramesh_patel", "email": "ramesh@farm.in", "farm": "Ramesh Organic Farm",
     "loc": "Nashik", "state": "Maharashtra", "phone": "9876543210",
     "bio": "Third-generation farmer growing organic vegetables for 25+ years."},
    {"username": "sunita_devi", "email": "sunita@farm.in", "farm": "Sunita Dairy & Greens",
     "loc": "Anand", "state": "Gujarat", "phone": "9876543211",
     "bio": "Fresh A2 milk, ghee, and seasonal greens from our family dairy."},
    {"username": "krishnan_m", "email": "krishnan@farm.in", "farm": "Krishnan Hill Farms",
     "loc": "Wayanad", "state": "Kerala", "phone": "9876543212",
     "bio": "Spice garden in the Western Ghats — pepper, cardamom, coffee."},
    {"username": "gurpreet_singh", "email": "gurpreet@farm.in", "farm": "Punjab Wheat Co.",
     "loc": "Ludhiana", "state": "Punjab", "phone": "9876543213",
     "bio": "Premium wheat, basmati rice, and pulses from Punjab's fertile plains."},
    {"username": "laxmi_reddy", "email": "laxmi@farm.in", "farm": "Laxmi Fruit Orchards",
     "loc": "Ratnagiri", "state": "Maharashtra", "phone": "9876543214",
     "bio": "Alphonso mangoes, chikoos, and pomegranates straight from the orchard."},
    {"username": "bhaskar_rao", "email": "bhaskar@farm.in", "farm": "Bhaskar Honey Apiary",
     "loc": "Coorg", "state": "Karnataka", "phone": "9876543215",
     "bio": "Wild forest honey harvested ethically from Coorg's dense forests."},
]

CUSTOMERS = [
    {"username": "priya_sharma", "email": "priya@gmail.com", "first": "Priya", "last": "Sharma"},
    {"username": "arjun_mehta", "email": "arjun@gmail.com", "first": "Arjun", "last": "Mehta"},
    {"username": "neha_verma", "email": "neha@gmail.com", "first": "Neha", "last": "Verma"},
    {"username": "vikram_joshi", "email": "vikram@gmail.com", "first": "Vikram", "last": "Joshi"},
    {"username": "ananya_iyer", "email": "ananya@gmail.com", "first": "Ananya", "last": "Iyer"},
]

# Products: (category_slug, farmer_username, name, description, price, mrp, unit, stock, organic, featured)
PRODUCTS = [
    # Vegetables
    ("vegetables", "ramesh_patel", "Fresh Tomatoes", "Vine-ripened red tomatoes, hand-picked daily. Perfect for curries, salads, and sauces.", 40, 60, "kg", 150, False, True),
    ("vegetables", "ramesh_patel", "Organic Spinach", "Tender baby spinach leaves grown without pesticides. Rich in iron and vitamins.", 30, 45, "bundle", 80, True, True),
    ("vegetables", "ramesh_patel", "Green Capsicum", "Crisp, thick-walled capsicum. Ideal for stir-fries and stuffed dishes.", 60, 80, "kg", 100, False, False),
    ("vegetables", "sunita_devi", "Fresh Cauliflower", "Snow-white cauliflower heads with tight florets. Farm fresh.", 35, 50, "piece", 60, False, False),
    ("vegetables", "ramesh_patel", "Organic Carrots", "Sweet, crunchy orange carrots. Great for juices and salads.", 55, 70, "kg", 120, True, False),
    ("vegetables", "ramesh_patel", "Bitter Gourd", "Fresh karela with deep green skin. Best for traditional recipes.", 45, 60, "kg", 70, False, False),
    ("vegetables", "sunita_devi", "Okra (Bhindi)", "Tender lady fingers, perfect for crispy fry.", 50, 65, "kg", 90, False, False),
    ("vegetables", "ramesh_patel", "Organic Cucumber", "Cool, crisp cucumbers grown organically. Hydrating and fresh.", 40, 55, "kg", 140, True, False),

    # Fruits
    ("fruits", "laxmi_reddy", "Alphonso Mangoes", "GI-tagged Ratnagiri Alphonso — the king of mangoes. Sweet, aromatic, premium quality.", 450, 600, "dozen", 40, False, True),
    ("fruits", "laxmi_reddy", "Fresh Pomegranates", "Ruby-red arils, juicy and sweet. Rich in antioxidants.", 120, 150, "kg", 80, False, True),
    ("fruits", "laxmi_reddy", "Sweet Chikoo", "Creamy, caramel-flavored sapota from Konkan orchards.", 80, 100, "kg", 60, False, False),
    ("fruits", "laxmi_reddy", "Bananas (Elaichi)", "Small, fragrant, extra-sweet elaichi bananas.", 50, 70, "dozen", 200, False, False),
    ("fruits", "laxmi_reddy", "Fresh Guavas", "Firm, aromatic guavas with pink flesh. High in Vitamin C.", 70, 90, "kg", 100, False, False),
    ("fruits", "laxmi_reddy", "Nagpur Oranges", "Juicy Nagpur santra — sweet and easy to peel.", 90, 120, "kg", 90, False, False),

    # Dairy & Eggs
    ("dairy", "sunita_devi", "A2 Cow Milk", "Pure A2 milk from indigenous Gir cows. Delivered fresh daily.", 80, 100, "litre", 50, True, True),
    ("dairy", "sunita_devi", "Farm Fresh Paneer", "Soft, crumbly paneer made from fresh cow milk. Perfect for curries.", 400, 480, "kg", 30, True, True),
    ("dairy", "sunita_devi", "Desi Cow Ghee", "Golden bilona ghee churned from A2 milk. Rich aroma.", 1200, 1500, "kg", 25, True, True),
    ("dairy", "sunita_devi", "Farm Eggs (Free Range)", "Free-range brown eggs from pasture-raised hens.", 90, 120, "dozen", 100, False, False),
    ("dairy", "sunita_devi", "Fresh Curd", "Thick, creamy curd set in earthen pots.", 60, 80, "kg", 40, True, False),
    ("dairy", "sunita_devi", "White Butter", "Hand-churned white butter from fresh cream.", 500, 600, "kg", 20, True, False),

    # Grains & Pulses
    ("grains", "gurpreet_singh", "Basmati Rice Premium", "Aged long-grain basmati with a distinct aroma. Perfect for biryani.", 180, 220, "kg", 500, False, True),
    ("grains", "gurpreet_singh", "Whole Wheat (Sharbati)", "Sharbati wheat from MP — high protein, golden grains.", 60, 75, "kg", 400, False, False),
    ("grains", "gurpreet_singh", "Toor Dal", "Premium quality split pigeon peas. Unpolished, high protein.", 160, 190, "kg", 200, False, False),
    ("grains", "gurpreet_singh", "Organic Moong Dal", "Yellow moong dal — light, easy to digest, organically grown.", 140, 170, "kg", 180, True, False),
    ("grains", "gurpreet_singh", "Chana Dal", "Bengal gram split dal, ideal for dal and snacks.", 120, 145, "kg", 250, False, False),
    ("grains", "gurpreet_singh", "Foxtail Millet", "Ancient grain, low GI, great for diabetes-friendly diets.", 120, 150, "kg", 100, True, False),
    ("grains", "gurpreet_singh", "Pearl Millet (Bajra)", "Fresh bajra, ideal for winter rotis.", 55, 70, "kg", 300, False, False),

    # Spices & Herbs
    ("spices", "krishnan_m", "Black Pepper (Whole)", "Bold Malabar peppercorns, sun-dried. Intense aroma.", 900, 1100, "kg", 50, False, True),
    ("spices", "krishnan_m", "Green Cardamom", "Plump Alleppey cardamom pods. Fragrant and premium.", 2400, 2800, "kg", 20, False, True),
    ("spices", "krishnan_m", "Kashmiri Red Chili", "Bright red, mild heat. Ideal for tandoori and curries.", 400, 500, "kg", 60, False, False),
    ("spices", "krishnan_m", "Turmeric Powder", "High-curcumin Salem turmeric, stone-ground.", 220, 280, "kg", 100, False, False),
    ("spices", "krishnan_m", "Cinnamon Sticks", "True Ceylon cinnamon — sweet and delicate.", 600, 750, "kg", 40, False, False),
    ("spices", "krishnan_m", "Fresh Curry Leaves", "Aromatic curry patta, freshly plucked.", 20, 30, "bundle", 200, False, False),
    ("spices", "krishnan_m", "Coriander Seeds", "Whole dhania seeds, sun-dried and aromatic.", 150, 190, "kg", 120, False, False),

    # Honey & Preserves
    ("honey", "bhaskar_rao", "Wild Forest Honey", "Raw, unprocessed honey from Coorg forests. Multiflora.", 650, 800, "kg", 80, True, True),
    ("honey", "bhaskar_rao", "Organic Jamun Honey", "Single-origin honey from Jamun blossoms. Dark, rich, medicinal.", 850, 1000, "kg", 40, True, True),
    ("honey", "bhaskar_rao", "Homemade Mango Jam", "Slow-cooked Alphonso pulp with jaggery. No preservatives.", 350, 420, "kg", 50, True, False),
    ("honey", "bhaskar_rao", "Mixed Fruit Pickle", "Traditional recipe, sun-cured with mustard oil and spices.", 280, 350, "kg", 60, True, False),
    ("honey", "bhaskar_rao", "Organic Bee Pollen", "Nutrient-dense raw bee pollen granules.", 1200, 1500, "kg", 25, True, False),
    ("honey", "bhaskar_rao", "Beeswax (Natural)", "Pure beeswax blocks for skincare and crafts.", 500, 650, "kg", 30, True, False),

    # Organic Specials
    ("organic", "ramesh_patel", "Organic Quinoa", "Premium white quinoa, organically grown.", 350, 450, "kg", 70, True, True),
    ("organic", "ramesh_patel", "Chia Seeds", "Raw organic chia seeds, high omega-3.", 400, 500, "kg", 80, True, False),
    ("organic", "sunita_devi", "Organic Jaggery Powder", "Chemical-free jaggery from organic sugarcane.", 120, 150, "kg", 100, True, False),
    ("organic", "gurpreet_singh", "Organic Brown Rice", "Unpolished brown rice, high fiber.", 130, 160, "kg", 150, True, False),

    # Flowers
    ("flowers", "krishnan_m", "Jasmine Flowers", "Fragrant Malli poo, freshly harvested every morning.", 200, 250, "bundle", 60, False, False),
    ("flowers", "krishnan_m", "Marigold Garland", "Fresh orange-yellow marigold, 2 ft long.", 100, 130, "piece", 50, False, False),
    ("flowers", "laxmi_reddy", "Rose Stems (Red)", "Long-stem red roses, cut fresh today.", 300, 400, "bundle", 40, False, False),
    ("flowers", "krishnan_m", "Tulsi Sapling", "Holy basil sapling in a pot, ready to plant.", 80, 100, "piece", 80, False, False),
]

REVIEW_COMMENTS = {
    5: ["Absolutely fresh and delicious!", "Best quality I've had in years.", "Will definitely reorder. Superb!",
        "Exceeded expectations. Fresh and aromatic.", "Worth every rupee!"],
    4: ["Good quality, will buy again.", "Fresh and well-packed.", "Nice product, delivery was quick.",
        "Quality is great, slight delay in shipping."],
    3: ["Decent product, average quality.", "Okay for the price.", "Not bad, but expected better freshness."],
    2: ["Quality was below expectation.", "Got slightly damaged on arrival."],
    1: ["Very disappointed.", "Stale product received."],
}

REVIEW_TITLES = ["Excellent!", "Very Good", "Good", "Okay", "Not Satisfied",
                 "Loved it", "Fresh & Tasty", "Highly Recommend", "Average", "Will Reorder"]


class Command(BaseCommand):
    help = "Seed the database with realistic demo data for FarmDirect."

    def add_arguments(self, parser):
        parser.add_argument('--fresh', action='store_true',
                            help='Delete all existing demo data before seeding')
        parser.add_argument('--seed', type=int, default=42,
                            help='Random seed for reproducibility')

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(options['seed'])

        if options['fresh']:
            self.stdout.write(self.style.WARNING("Wiping existing demo data..."))
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            CartItem.objects.all().delete()
            Cart.objects.all().delete()
            Review.objects.all().delete()
            Product.objects.all().delete()
            FarmerProfile.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        # ---------- Categories ----------
        self.stdout.write("Creating categories...")
        cat_map = {}
        for c in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                name=c['name'],
                defaults={
                    'slug': c['slug'],
                    'icon': c['icon'],
                    'description': c['description'],
                }
            )
            # Force-update slug in case an old row exists without it
            if cat.slug != c['slug']:
                cat.slug = c['slug']
                cat.save()
            cat_map[c['slug']] = cat

        # ---------- Farmers ----------
        self.stdout.write("Creating farmers...")
        farmer_map = {}
        for f in FARMERS:
            user, created = User.objects.get_or_create(
                username=f['username'],
                defaults={
                    'email': f['email'],
                    'first_name': f['farm'].split()[0],
                    'last_name': 'Farmer',
                    'is_staff': False,
                }
            )
            if created:
                user.set_password('farmer123')
                user.save()
            profile, _ = FarmerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'farm_name': f['farm'],
                    'location': f['loc'],
                    'state': f['state'],
                    'phone': f['phone'],
                    'bio': f['bio'],
                    'is_verified': True,
                    'rating': Decimal(str(round(random.uniform(4.2, 4.9), 2))),
                }
            )
            farmer_map[f['username']] = user

        # ---------- Customers ----------
        self.stdout.write("Creating customers...")
        customer_map = {}
        for c in CUSTOMERS:
            user, created = User.objects.get_or_create(
                username=c['username'],
                defaults={
                    'email': c['email'],
                    'first_name': c['first'],
                    'last_name': c['last'],
                }
            )
            if created:
                user.set_password('customer123')
                user.save()
            customer_map[c['username']] = user

        # ---------- Products ----------
        self.stdout.write("Creating products...")
        products = []
        today = date.today()
        for (cat_slug, farmer_un, name, desc, price, mrp, unit, stock, organic, featured) in PRODUCTS:
            farmer = farmer_map[farmer_un]
            category = cat_map[cat_slug]
            harvest = today - timedelta(days=random.randint(1, 10))
            p, created = Product.objects.get_or_create(
                name=name,
                farmer=farmer,
                defaults={
                    'category': category,
                    'description': desc,
                    'short_description': desc[:150],
                    'price': Decimal(str(price)),
                    'mrp': Decimal(str(mrp)),
                    'unit': unit,
                    'stock': stock,
                    'is_organic': organic,
                    'is_featured': featured,
                    'is_available': True,
                    'harvest_date': harvest,
                    'image_url': f"https://source.unsplash.com/400x400/?{name.replace(' ', ',').lower()}",
                }
            )
            products.append(p)

        # ---------- Reviews ----------
        self.stdout.write("Creating reviews...")
        customer_list = list(customer_map.values())
        for product in products:
            # Each product gets 2-5 reviews
            num_reviews = random.randint(2, 5)
            reviewers = random.sample(customer_list, min(num_reviews, len(customer_list)))
            for customer in reviewers:
                rating = random.choices([5, 4, 3, 2, 1], weights=[50, 30, 12, 5, 3])[0]
                Review.objects.get_or_create(
                    product=product, user=customer,
                    defaults={
                        'rating': rating,
                        'title': random.choice(REVIEW_TITLES),
                        'comment': random.choice(REVIEW_COMMENTS[rating]),
                    }
                )

        # ---------- Carts (live demo carts) ----------
        self.stdout.write("Creating carts...")
        for customer in customer_list[:3]:
            cart, _ = Cart.objects.get_or_create(user=customer)
            cart.items.all().delete()
            for product in random.sample(products, k=random.randint(2, 4)):
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=random.randint(1, 3),
                )

        # ---------- Orders (historical) ----------
        self.stdout.write("Creating order history...")
        cities = [
            ("Mumbai", "Maharashtra", "400001"),
            ("Delhi", "Delhi", "110001"),
            ("Bangalore", "Karnataka", "560001"),
            ("Chennai", "Tamil Nadu", "600001"),
            ("Pune", "Maharashtra", "411001"),
            ("Hyderabad", "Telangana", "500001"),
        ]
        statuses = ['delivered', 'delivered', 'delivered', 'shipped', 'confirmed', 'pending', 'cancelled']

        for customer in customer_list:
            for _ in range(random.randint(2, 5)):
                city, state, pin = random.choice(cities)
                days_ago = random.randint(1, 60)
                order_date = timezone.now() - timedelta(days=days_ago)

                # Pick 1-4 products
                order_products = random.sample(products, k=random.randint(1, 4))
                subtotal = Decimal('0')
                item_data = []
                for product in order_products:
                    qty = random.randint(1, 3)
                    line_total = product.price * qty
                    subtotal += line_total
                    item_data.append((product, qty, line_total))

                delivery_fee = Decimal('40') if subtotal < Decimal('500') else Decimal('0')
                total = subtotal + delivery_fee

                order = Order.objects.create(
                    user=customer,
                    full_name=f"{customer.first_name} {customer.last_name}",
                    phone=f"9{random.randint(100000000, 999999999)}",
                    address=f"{random.randint(1, 999)}, {random.choice(['MG Road', 'Nehru Nagar', 'Gandhi Street', 'Park Avenue'])}",
                    city=city, state=state, pincode=pin,
                    payment_method=random.choice(['cod', 'upi', 'card']),
                    subtotal=subtotal,
                    delivery_fee=delivery_fee,
                    total_amount=total,
                    status=random.choice(statuses),
                    created_at=order_date,
                )
                # Override auto_now_add
                Order.objects.filter(id=order.id).update(created_at=order_date)

                for product, qty, line_total in item_data:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        price=product.price,
                        quantity=qty,
                        farmer=product.farmer,
                    )

        # ---------- Superuser ----------
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@farmdirect.in', 'admin123')
            self.stdout.write(self.style.SUCCESS("Superuser created: admin / admin123"))

        # ---------- Summary ----------
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 60))
        self.stdout.write(self.style.SUCCESS("✅ DEMO DATA SEEDED SUCCESSFULLY"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(f"  Categories : {Category.objects.count()}")
        self.stdout.write(f"  Farmers    : {FarmerProfile.objects.count()}")
        self.stdout.write(f"  Products   : {Product.objects.count()}")
        self.stdout.write(f"  Customers  : {User.objects.filter(is_superuser=False, farmer_profile__isnull=True).count()}")
        self.stdout.write(f"  Reviews    : {Review.objects.count()}")
        self.stdout.write(f"  Carts      : {Cart.objects.count()}")
        self.stdout.write(f"  Orders     : {Order.objects.count()}")
        self.stdout.write(f"  OrderItems : {OrderItem.objects.count()}")
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write("\n🔑 LOGIN CREDENTIALS")
        self.stdout.write("  Admin    : admin / admin123")
        self.stdout.write("  Farmer   : ramesh_patel / farmer123")
        self.stdout.write("  Customer : priya_sharma / customer123")
        self.stdout.write(self.style.SUCCESS("=" * 60 + "\n"))