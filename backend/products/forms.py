from django import forms
from .models import ProductCategory, Product, Review


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter category description'}),
            'created_at': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'stock_quantity', 'image', 'is_active', 'created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'created_at': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES, attrs={'class': 'form-check-input'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this product...'
            }),
        }
