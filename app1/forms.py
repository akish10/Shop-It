
from django import forms 

from django.contrib.auth.models import User 

from django.contrib.auth.forms import UserCreationForm

from .models import AddItem

from .models import *

class UserForm(UserCreationForm):

    first_name = forms.CharField()

    last_name = forms.CharField()

    email = forms.EmailField()


    class Meta:

        model = User

        fields = ('first_name', 'last_name','username','email','password1','password2')


class LoginForm(forms.Form):
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class AddItemForm(forms.ModelForm):

    class Meta:

        model = AddItem

        exclude = ['username']

        fields = ['item_name', 'quantity','price','location','image','description']


class BoughtItem(forms.ModelForm):

    class Meta:

        model = BoughtItem


        fields = ['buyer','item_bought','quantity_bought','price_bought']

        

class UpdateItemDetails(forms.ModelForm):

    class Meta:

        model = UpdateItemDetails


        fields = ['seller_update','item_update','quantity_update','reset_price','reset_description']


class Transactions(forms.ModelForm):

    class Meta:

        model = Transactions

        fields = ['item_paid','quantity_paid','buyer_paid']

class PayForm(forms.ModelForm):

    class Meta:

        model = Pay

        fields = ['phone_number','name','amount','transaction_status']


class OrderForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = ['item', 'quantity']