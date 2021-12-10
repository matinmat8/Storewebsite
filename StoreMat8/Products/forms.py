from django import forms
from Products.models import DiscountSystem


class SearchForm(forms.Form):
    search = forms.CharField()


class DiscountCode(forms.ModelForm):
    class Meta:
        model = DiscountSystem
        fields = ['discount_code']
