from django.contrib.auth import get_user_model
from django.shortcuts import render
from braces.views import SelectRelatedMixin
from django.views import generic
from . import models

# Create your views here.
User = get_user_model()

class OrderList(SelectRelatedMixin,generic.ListView):
    model = models.Order
    select_related=('user', 'description')

class UserOrders(generic.ListView):
    model = models.Order
    template_name = 'orders/user_order_list.html'

class CreateOrder(SelectRelatedMixin,generic.CreateView):
    fields = {'vehicle','description'}

class OrderDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Order
    select_related = ("user")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


