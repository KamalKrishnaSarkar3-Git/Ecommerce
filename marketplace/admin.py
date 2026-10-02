from django.contrib import admin
from django.utils.html import format_html
from .models import (Category, Product, Cart, CartItem, Order, OrderItem,
                     FarmerProfile, Review)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'user', 'location', 'state', 'is_verified', 'rating')
    list_filter = ('is_verified', 'state')
    search_fields = ('farm_name', 'user__username', 'location')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'name', 'farmer', 'category', 'price', 'mrp',
                    'stock', 'is_organic', 'is_featured', 'is_available')
    list_filter = ('is_organic', 'is_featured', 'is_available', 'category')
    search_fields = ('name', 'description', 'farmer__username')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_available', 'is_featured')
    list_per_page = 30

    def thumb(self, obj):
        url = obj.image.url if obj.image else obj.image_url
        if url:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;">', url)
        return "—"
    thumb.short_description = "Image"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'farmer')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'city', 'total_amount',
                    'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('id', 'user__username', 'full_name', 'phone')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    date_hierarchy = 'created_at'


admin.site.register(Cart)
admin.site.register(CartItem)