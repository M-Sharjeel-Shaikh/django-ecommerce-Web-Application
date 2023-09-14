from django.db import models
from django.contrib.auth.models import User
from store.models import ColorVariant, Product, SizeVariant

# Model Here:
class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified= models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    

class Favourite(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorites')
    favourite = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return str(self.user)

    

class Cart(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color_varient = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_varient = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Ordered(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    payment_no = models.CharField(max_length=30, null=True, blank=True)
    payment_ref = models.CharField(max_length=30, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

