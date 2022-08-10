 
from django import forms

from .models import Reviews

class ReviewForm(forms.ModelForm):
    """komment uchun forma"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')
