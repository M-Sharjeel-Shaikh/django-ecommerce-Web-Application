# Create your models here.
from django.db import models
import uuid
from django.contrib.auth.models import User
from .util import unique_slug_generator
from ckeditor.fields import RichTextField

# Extra modification by built-in method 
# from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator



class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        abstract = True 



class Seller(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    


class ColorVariant(models.Model):
    color_name = models.CharField(max_length=100)
    price=models.IntegerField(default=0)

    def __str__(self):
        return self.color_name



class SizeVariant(models.Model):
    size_name = models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    
    def __str__(self):
        return self.size_name  
    


from django.db.models.signals import pre_save
from django.dispatch import receiver

class Product(BaseModel):
    name = models.CharField(max_length=1000)
    description = models.TextField(max_length=2500)
    title = models.TextField(max_length=150, null="None")
    information = RichTextField()
    price = models.FloatField(default=0)
    discount_price = models.IntegerField(default=0)
    image = models.ImageField(null=True, upload_to='media/')
    extra_image = models.ImageField(null=True, blank = True,upload_to='media/')
    display_image = models.ImageField(upload_to='media/')
    slug = models.SlugField(unique=True , null=True , blank=True) 
    rating=models.IntegerField(default=0)   
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    color_variant = models.ManyToManyField(ColorVariant , blank=True, related_name="variant")
    size_variant = models.ManyToManyField(SizeVariant , blank=True, related_name="variant")
    
    CATEGORY_CHOICES = ( 
        ("1", "Men's Dresses"), 
        ("2", "Women's Dresses"), 
        ("3", "Baby's Dresses"), 
        ("4", "Shirts"), 
        ("5", "Jeans"), 
        ("6", "Furniture/Equipment"), 
        ("7", "Digital Products"), 
        ("8", "Watches"), 
        ("9", "Household"), 
        ("10", "MakeUp Products"),
        ("11", "Jackets"),
        ("12", "Shoes"),
    ) 
    
    category = models.CharField( 
        max_length = 20, 
        choices = CATEGORY_CHOICES, 
        default = '1'
        )
    
    def __str__(self):
        return self.name

    # def average_review(self):
    #     reviews = Review.objects.filter(product=self).aggregate(average=Avg('rate'))
    #     avg = 0

    #     if reviews['average'] is not None:
    #         avg = int(reviews['average'])
        
    # def save(self, **kwargs):
    #     reviews = Review.objects.filter(product=self).aggregate(average=Avg('rate'))
    #     avg = 0

    #     if reviews['average'] is not None:
    #         avg = int(reviews['average'])

    #     super(Product, self).save(**kwargs)
    #     return avg

    # def save(self, **kwargs):
    #     super(Product, self).save(**kwargs)
    #     return avg


@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class ProductImage(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="images")
    image =  models.ImageField(upload_to="media")

    
class Coupon(models.Model):
    code = models.CharField(max_length=30)
    value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField()


RATE_CHOICES = [
(1, '1 - Bad'),
(2, '2 - Poor'),
(3, '3 - Average'),
(4, '4 - Great'),
(5, '5 - Excellent'),
]


class Review(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  comment = models.TextField(max_length=500)
  rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

