from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from  .models import OrderedPart, Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ()


class OrderedPartForm(ModelForm):

    class Meta:
        model = OrderedPart
        exclude = ()


OrderedPartFormset = inlineformset_factory(Order, OrderedPart,
                                            form=OrderedPartForm, extra=1)
