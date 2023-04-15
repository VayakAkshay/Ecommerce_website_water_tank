from django.db import models
import datetime
# Create your models here.

class ProductData(models.Model):
    product_id = models.AutoField
    product_name = models.TextField(max_length=300,default="")
    product_desc = models.TextField(max_length=9000,default="")
    product_img = models.ImageField(upload_to="products")
    product_price = models.IntegerField(default=0)
    product_cat = models.TextField(max_length=100,default="")
    product_qty = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.product_name
    
class CartData(models.Model):
    cart_id = models.AutoField
    product_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    qty = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)

class WishlistData(models.Model):
    widhlist_id = models.AutoField
    product_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)

class ReviewData(models.Model):
    review_id = models.AutoField
    product_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    reviewer_name = models.TextField(max_length=200,default="")
    review_desc = models.TextField(max_length=5000,default="")
    date = models.DateField(default=datetime.date.today)
    review_star = models.IntegerField(default=0)
    
class OrderItem(models.Model):
    order_id = models.AutoField
    product_id = models.IntegerField(default=0)
    qty = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)