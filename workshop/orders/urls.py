from django.urls import re_path
from orders import views

app_name = 'orders'

urlpatterns = [
    re_path(r'new/$',views.CreateOrder.as_view(),name='create'),
    re_path(r"^$", views.OrderList.as_view(), name="all_orders"),
    re_path(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$", views.OrderDetail.as_view(), name="single"),
]