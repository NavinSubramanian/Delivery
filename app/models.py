from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    workertype = models.CharField(max_length=50, default='0')

    def __str__(self):
        return self.username
    
class Category(models.Model):
    category = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.category
    
class Item(models.Model):
    itemname = models.CharField(max_length=50,null=True)
    cost = models.CharField(max_length=50)
    perish = models.CharField(max_length=50)
    expiry = models.CharField(max_length=100,default='None')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)

    def get_stock_count(self):
        return self.inventory_set.filter(itemname=self, username=None).count()

    def __str__(self):
        return self.itemname
    
class Inventory(models.Model):
    itemname = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    stock = models.CharField(max_length=50)

    def __str__(self):
        return self.stock
    
class Request(models.Model):
    itemname = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    requester = models.CharField(max_length=50)
    needed = models.CharField(max_length=50)
    username = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.requester
