from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, FarmerProfile, Order, Review


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_farmer = forms.BooleanField(required=False, label="Register as Farmer")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['farm_name', 'location', 'phone', 'bio']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'unit',
                  'stock', 'image', 'is_organic', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address', 'city', 'pincode']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} ★") for i in range(5, 0, -1)],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial=5,
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Summary (optional)'}),
        }