from attr import field
from django import forms
from . models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.TextInput(attrs={'class': 'form-control'})
        }