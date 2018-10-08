from django.contrib import admin
from .models import Order, Part, OrderedPart

admin.site.register(Order)
admin.site.register(Part)
admin.site.register(OrderedPart)
