from django import forms

from .models import Product, Category, Comments


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "current_price",
            "image",
            "image_url",
            "category",
        )
        labels = {
            "title": "Title",
            "description": "Description",
            "current_price": "Bid",
            "image": "Image",
            "image_url": "Image Url",
            "category": "Category",
        }


class CommentForm(forms.Form):
    name = forms.CharField()
    body = forms.CharField()
