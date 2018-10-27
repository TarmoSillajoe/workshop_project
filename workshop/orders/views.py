from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib import messages
from django.views import generic
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
from .models import Order, Part, OrderedPart

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
    fields = ['description', 'vehicle']


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
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            form.save()
        
        if orderedparts.is_valid():
            orderedparts.instance = self.object
            orderedparts.save()
        print(orderedparts.cleaned_data)
        return super(OrderOrderedPartCreate, self).form_valid(form)
        

class OrderOrderedPartUpdate(SingleObjectMixin, FormView,LoginRequiredMixin,SelectRelatedMixin):
    model = Order
    fields = ['vehicle', 'description']
    success_url = reverse_lazy('orders:all_orders')

    def get_context_data(self, **kwargs):
        data = super(OrderOrderedPartUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orderedparts'] = OrderedPartFormset(self.request.POST, instance=self.object)
        else:
            data['orderedparts'] = OrderedPartFormset(instance=self.object)
        return data
            

    def form_valid(self, form):
        context = self.get_context_data()
        parts = context['orderedparts']
        with transaction.atomic():
            self.object = form.save()

            if orderedparts.is_valid():
                orderedparts.instance = self.object
                orderedparts.save()
        return super(OrderOrderedPartUpdateView, self).form_valid(form)


class OrderDetail(SelectRelatedMixin, generic.DetailView):
    model = Order
    select_related = ('user',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))
