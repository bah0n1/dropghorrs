from typing import List
from django.contrib import admin
from .models import Customer,Affiliater,Reseller,Product_Catagorie,Product,Afflink,Cart,Order_Status,User_otp,Product_Price_and_attribute
# Register your models here.

@admin.register(Customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ("id","user","name","number","locality","city")

@admin.register(Affiliater)
class customerAdmin(admin.ModelAdmin):
    list_display = ("id","user","name","rank","sales","appli")

@admin.register(Reseller)
class ResellerAdmin(admin.ModelAdmin):
    list_display = ("id","user","nid_num","profile_pic","appli")

@admin.register(Product_Catagorie)
class Product_CatAdmin(admin.ModelAdmin):
    list_display = ("id","catagorie")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","catagorie","description","discount_rate","star")

@admin.register(Afflink)
class AfflinkAdmin(admin.ModelAdmin):
    list_display = ("id","affler","product")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id","user","product","Pro_price_att",'quantity',"reffer")


@admin.register(Order_Status)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id","user","customer","product","order_date",'quantity',"status")


@admin.register(User_otp)
class User_otpAdmin(admin.ModelAdmin):
    list_display = ("id","user","otp")

@admin.register(Product_Price_and_attribute)
class pro_pricandattAdmin(admin.ModelAdmin):
    list_display = ("id","product","att","price")

