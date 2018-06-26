from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=100)
    vehicle = models.CharField(max_length=100)
    
    def save(self,*args,**kwargs):
        super( ).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('orders:single',
                       kwargs={
                            'username': self.user.name,
                            'pk':self.pk
                            }
        )


class Part(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return "{0}; {1}".format(self.code, self.description)

class OrderedPart(models.Model):
    part = models.OneToOneField( Part,
        on_delete=models.CASCADE,
        primary_key=True)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='parts', null=True,blank=True,on_delete=models.CASCADE)
