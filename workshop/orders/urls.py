from django.urls import re_path, path
from orders import views


app_name = 'orders'

urlpatterns = [
    re_path(r'new/$',views.OrderOrderedPartCreate.as_view(),name='order-add'),
    path('order/<int:pk>/edit/',
        views.OrderOrderedPartUpdate.as_view(),
        name='order_parts_update'),
    re_path(r"^$", views.OrderList.as_view(), name="all_orders"),
    re_path(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$", views.OrderDetail.as_view(), name="single"),
]