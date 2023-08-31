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

    def __str__(self):
        return self.user.id
    

class Favourite(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorites')
    favourite = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    

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
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

