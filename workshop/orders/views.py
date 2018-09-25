from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from braces.views import SelectRelatedMixin

from django.views.generic import (
    CreateView, DetailView, FormView, ListView, TemplateView
)
from django.views.generic.detail import SingleObjectMixin

from .forms import OrderedPartFormset
from .models import Order, OrderedPart

# Create your views here.
User = get_user_model()

class OrderList(SelectRelatedMixin, ListView):
    model = Order

    select_related=('user',)


class UserOrders(ListView):
    model = Order
    template_name = 'orders/user_order_list.html'

    def get_queryset(self):
        try:
            self.order_user = User.objects.prefetch_related('orders').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.order_user.orders.all()


class OrderCreateView(CreateView, LoginRequiredMixin,SelectRelatedMixin):
    model = Order
    #template_name = 'orders/order_form.html'
    #success_url = reverse_lazy('orders:all_orders')
    fields = ['part', 'quantity']


class OrderOrderedPartCreate(CreateView):
    model = Order
    fields = ['description', 'vehicle']
    success_url = reverse_lazy('orders:all_orders')
    
    #template_name = 'orders/order_form.html'

    def get_context_data(self, **kwargs):
        data = super(OrderOrderedPartCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orderedparts'] = OrderedPartFormset(self.request.POST)
        else:
            data['orderedparts'] = OrderedPartFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderedparts = context['orderedparts']
        with transaction.atomic():
            self.object = form.save()

        if orderedparts.is_valid():
            orderedparts.instance = self.objects
            orderedparts.save()
        return super(OrderOrderedPartCreate, self).form.form_valid(form)
        

class OrderOrderedPartUpdateView(SingleObjectMixin, FormView,LoginRequiredMixin,SelectRelatedMixin):
    model = Order
    fields = ['vehicle', 'description']
    success_url = reverse_lazy('orders:all_orders')

    def get_context_data(self, **kwargs):
        data = super(ProfileFamilyMemberUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orderedparts'] = OrderedPartFormset(self.request.POST, instance=self.object)
        else:
            data['orderedparts'] = OrderedPartFormset(instance=self.object)
        return data
            

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['orderedparts']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(OrderOrderedPartUpdateView, self).form_valid(form)

