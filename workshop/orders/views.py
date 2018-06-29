from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views import generic
from . import models
from . import forms

# Create your views here.
User = get_user_model()

class OrderList(SelectRelatedMixin,generic.ListView):
    model = models.Order
    select_related=('user', 'description')

class UserOrders(generic.ListView):
    model = models.Order
    template_name = 'orders/user_order_list.html'

    def get_queryset(self):
        try:
            self.order_user = User.objects.prefetch_related('orders').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.order_user.orders.all()

class CreateOrder(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
   #  form_class = forms.OrderCreateForm
    fields = ['vehicle','description']
    model = models.Order

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
        


class OrderDetail(generic.DetailView):
    model = models.Order
    #select_related = ("user")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


