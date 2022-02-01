from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.expressions import Case
from django.db.models.query_utils import check_rel_lookup_compatibility
from django.core.exceptions import ValidationError
from matplotlib.pyplot import title
from sqlalchemy import true


# all validator

# product description min length validator
def des_min(value):
    if len(value) < 45:
        raise ValidationError("product description should be bigger than 45 character")
    else:
        return value





# end validator

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    number=models.IntegerField()
    locality=models.CharField(max_length=35)
    city=models.CharField(max_length=20)


    def __str__(self):
        return(str(self.name))



AFFI_APP_CHOICES=(
    ("REQ","REQUEST"),
    ("AP","APPROVED"),
    ("CUS","CUSTOMER")

)

class Affiliater(models.Model):
    user=models.OneToOneField(User,on_delete=models.Case)
    name=models.OneToOneField(Customer,on_delete=models.Case)
    rank=models.IntegerField(default=1)
    sales=models.IntegerField(default=0)
    appli=models.CharField(choices=AFFI_APP_CHOICES,max_length=20,default="REQUEST")

    def __str__(self):
        return str(self.name)


RESELLER_APP_CHOICES=(
    ("REQ","REQUEST"),
    ("AP","APPROVED"),
    ("CUS","CUSTOMER")

)

class Reseller(models.Model):
    user=models.OneToOneField(User,on_delete=models.Case)
    nid_num=models.IntegerField()
    profile_pic=models.ImageField(upload_to="profile_img")
    appli=models.CharField(choices=RESELLER_APP_CHOICES,max_length=20,default="REQUEST")


    def __str__(self):
        return str(self.id)



class Product_Catagorie(models.Model):
    catagorie=models.CharField(max_length=25,unique=True)
    # description=models.CharField(max_length=58,validators=[des_min])

    def __str__(self):
        return str(self.catagorie)



class Product(models.Model):
    name = models.CharField(max_length=15)
    product_pic=models.ImageField(upload_to="product_img")
    catagorie=models.ForeignKey(Product_Catagorie,on_delete=CASCADE)
    titel=models.CharField(max_length=58,validators=[des_min])
    description=models.CharField(max_length=290)
    discount_rate=models.FloatField(null=True,blank=True)
    star=models.FloatField()

    def __str__(self):
        return str(self.name)
    @property
    def check_flot(self):
        if isinstance(self.star,int):
            return self.star
        else:
            return self.star
class Product_Price_and_attribute(models.Model):
    product=models.ForeignKey(Product,on_delete=CASCADE)
    att=models.CharField(max_length=30)
    price=models.FloatField()

    def __str__(self):
        return str(self.price)

# AFFILIATE LINK
class Afflink(models.Model):
    affler=models.ForeignKey(Affiliater,on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)

    def __str__(self):
        return str(self.affler.user)


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    Pro_price_att=models.ForeignKey(Product_Price_and_attribute,on_delete=CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    reffer=models.ForeignKey(Afflink,on_delete=CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.product.name)



ORDER_STATUS=(

    ("pending","pending"),
    ("accepted","accepted"),
    ("cancel","cancel"),
    ("prepairing","prepairing"),
    ("on the way","on the way"),
    ("delivered","delivered")
)

class Order_Status(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Cart,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    order_date_no_time=models.DateField(auto_now_add=True,null=True,blank=True)
    quantity=models.PositiveIntegerField(default=1)
    status=models.CharField(choices=ORDER_STATUS,max_length=20,default="pending")


    def __str__(self):
        return str(self.id)


class User_otp(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    time=models.DateTimeField(auto_now=True)
    otp=models.SmallIntegerField()

    def __str__(self):
        return str(self.id)




