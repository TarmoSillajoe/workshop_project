from django import forms
from .models import Order

class OrderCreateForm():

        class Meta:
            fields = ('description','vehicle')
            model = Order