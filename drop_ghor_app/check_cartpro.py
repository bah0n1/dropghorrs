from django.contrib.auth.models import User
from .models import Cart,Product

class Check_cart:
    def __init(self,pro_id,cus):
        self.pro_id = pro_id
        self.cus=cus

    def product(self):
        a=Cart.objects.filter(user=self.cus)
        if a:
            return True
        else:
            return False

if __name__ == '__main__':
    pr=Product.objects.get(pk=1)
    print("done")
    user=User.objects.get(pk=1)
    a=Check_cart(pro_id=pr,cus=user)
    print(a)