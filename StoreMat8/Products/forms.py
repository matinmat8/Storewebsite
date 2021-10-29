from django import forms


class SearchForm(forms.Form):
    search = forms.CharField()


class DiscountCode(forms.Form):
    discount_code = forms.CharField()