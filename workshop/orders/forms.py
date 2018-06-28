from django import forms

from orders import models


class OrderCreateForm(forms.ModelForm):

        class Meta:
            fields = ['vehicle','description']
            model = models.Order

        def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            
        