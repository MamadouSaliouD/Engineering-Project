from django.db import models
from django.contrib.auth.models import User
import pycountry

# Create your models here.
"""
class Users(models.Model):
    name = models.CharField(max_length=64, default=False)
    surname = models.CharField(max_length=64, default=False)
    username = models.CharField(max_length=64, default=False)
    COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=3, null=False, help_text="Please select an area code")
    city = models.CharField(max_length=64, default=False)
    created_time = models.DateTimeField(auto_now_add=True)
"""
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title =models.CharField(max_length =200)
    description = models.TextField(max_length=1000)
    STATUS_CHOICES = [('scheduled','Scheduled'),('completed','Completed'),('cancelled','Cancelled')]
    status = models.CharField(choices=STATUS_CHOICES, default='scheduled', max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_on = models.DateField(auto_now_add =True)


    def __str__(self):
        return f'{self.title}'
    
    def snippet(self):
        return self.description[:50] +'...'
    

