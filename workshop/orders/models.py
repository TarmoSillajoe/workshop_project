from django.db import models
from django.urls import reverse
from django.conf import settings

import misaka

from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User,related_name='orders',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    description = models.CharField(max_length=100)
    vehicle = models.CharField(max_length=100)

    def __str__(self):
        return self.description
    
    def save(self,*args,**kwargs):
        super( ).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('orders:single',
                       kwargs={
                            'username':self.user.username,
                            'pk':self.pk
                            }
        )


class Part(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    order = models.ManyToManyField(Order, through="OrderedPart")

    def __str__(self):
        return "{0}; {1}".format(self.code, self.description)

        
class OrderedPart(models.Model):
    part = models.ForeignKey(Part, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='parts',  on_delete=models.CASCADE)


