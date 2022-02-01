import datetime
import random
from django.core.mail import send_mail
from dropghor.settings import EMAIL_HOST_USER
from dropghor.settings import SECRET_KEY
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as logout_auth
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import LoginForm,CustomerRegistrationForm,ChangePassword,Customer_form
from .models import Product, User_otp,Customer,Product_Price_and_attribute,Cart,Afflink,Affiliater
from .hash_cookies import Afflink_cookie,Aff_url_maker


# Create your views here.
def index(request):
    pp= Product.objects.all()
    contex={"pp":pp}
    return render(request,"drop_ghor_app/index.html",contex)

def product(request):
    return render(request,"drop_ghor_app/product.html")

# login class
class login_cls(View):
    def get(self,request,*args, **kwargs):
        if not request.user.is_authenticated:
            fm=LoginForm()
            return render(request,"drop_ghor_app/login.html",{"fm":fm})
        else:
            return HttpResponseRedirect("/")
    def post(self, request, *args, **kwargs):
        get_otp=request.POST.get("otp")
        if get_otp:
            chek=otp(user=request.POST.get('usr'),otp=get_otp).check_otp()
            if chek[-1] == True:
                auth_login(request,User.objects.get(email=chek[0]))
                return HttpResponseRedirect("/")
            elif chek[-1] == None:
                return HttpResponseRedirect("/")
            else:
                messages.warning(request, f'You Entered a Wrong OTP')
                return render(request,"drop_ghor_app/registation.html",{"otp":True,"usr":chek[0]})
        else:
            fm=LoginForm(request.POST)
            if fm.is_valid():
                # user = authenticate(email=c, password=fm.cleaned_data["password"])
                user=self.log_cus(fm.cleaned_data["email"],fm.cleaned_data["password"])
                if user[-1] == True:
                    return HttpResponseRedirect("/")
                elif user[-1] =="deactive":
                    return render(request,"drop_ghor_app/login.html",{"otp":True,"usr":user[-2]})
                else:
                    messages.warning(request, f'You Entered a Wrong Email and Password if you forget your password you can reset it! ')
                    return HttpResponseRedirect("/login/")
            else:
                return render(request,"drop_ghor_app/login.html",{"fm":fm})
    
    def log_cus(self,cu_email,password):
        try:
            cus_email=User.objects.get(email=cu_email)
        except:
            cus_email=User.objects.filter(email=cu_email)
        if cus_email:
            flag=check_password(password,cus_email.password)
            if flag:
                if otp(cus_email).check_active() == True:
                    auth_login(self.request,cus_email)
                    return [True]
                else:
                    return [False,cus_email,"deactive"] 
            else:
                return [False]
        else:
            return [False]


# CUSTOMER REGISTATION CLASS
class Cus_reg(View):
    def get(self,request,*args, **kwargs):
        if not request.user.is_authenticated:
            fm = CustomerRegistrationForm()
            return render(request,"drop_ghor_app/registation.html",{"fm":fm})
        else:
            return HttpResponseRedirect("/")
    def post(self,request,*args, **kwargs):
        get_otp=request.POST.get("otp")
        if get_otp:
            chek=otp(user=request.POST.get('usr'),otp=get_otp).check_otp()
            if chek[-1] == True:
                messages.success(request, f'Account is Created For {chek[0]}')
                return HttpResponseRedirect("/login/")
            elif chek[-1] == None:
                return HttpResponseRedirect("/")
            else:
                messages.warning(request, f'You Entered a Wrong OTP')
                return render(request,"drop_ghor_app/registation.html",{"otp":True,"usr":chek[0]})
        else:  
            fm=CustomerRegistrationForm(request.POST)
            if fm.is_valid():
                fm.save()
                u_name=self.set_user_name(fm.cleaned_data["email"],fm.cleaned_data["first_name"],fm.cleaned_data["number"],fm.cleaned_data["address"],fm.cleaned_data["city"])
                send_otp=otp(User.objects.get(email=fm.cleaned_data["email"])).send_otp_mail()
                return render(request,"drop_ghor_app/registation.html",{"otp":True,"usr":User.objects.get(email=fm.cleaned_data["email"])})
            else:
                return render(request,"drop_ghor_app/registation.html",{"fm":fm})

    def set_user_name(self,email,first_name,cus_number=None,cus_address=None,cus_city=None):
        user=User.objects.get(email=email)
        suffix= datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        username="_".join([first_name,suffix])
        user.username=username
        user.is_active =False
        user.save()
        cus=Customer(user=user,name=first_name.capitalize(),number=cus_number,locality=cus_address.capitalize(),city=cus_city.capitalize())
        cus.save()


# otp generator and check

class otp:
    def __init__(self,user,otp=1):
        self.user =user
        self.otp=otp
    def send_otp_mail(self):
        ran_num=random.randint(100000,999999)
        User_otp.objects.create(user=self.user,otp=ran_num)
        mess=f"Hello {self.user.first_name.capitalize()},\nYour OTP is {ran_num}\nThanks!"
        send_mail(
                    "Welcome to DropGhor - Verify Your Email",
                    mess,
                    EMAIL_HOST_USER,
                    [self.user.email],
                    fail_silently = False
                    )
    def check_otp(self):
        user_cr=User.objects.get(username=self.user)
        try:
            if int(self.otp) == User_otp.objects.filter(user = user_cr).last().otp:
                user_cr.is_active = True
                user_cr.save()
                User_otp.objects.filter(user = user_cr).delete()
                return [user_cr.email,user_cr,True]
            else:
                return [User.objects.get(username=self.user),False]
        except:
            return [User.objects.get(username=self.user),False,None]
    def check_active(self):
        if User.objects.get(username=self.user).is_active == False:
            self.send_otp_mail()
            return False
        else:
            return True



# user profile edit

class Profile_View(View):
    def get(self,request):
        if request.user.is_authenticated:
            btn="btn-primary"
            pk=Customer.objects.get(user=request.user)
            form=Customer_form(instance=pk)
            return render(request, 'drop_ghor_app/profile.html',{"fm":form,"btn":btn})
        else:
            return HttpResponseRedirect("/login/")

    def post(self,request):
        pk=Customer.objects.get(user=request.user)
        fm=Customer_form(request.POST,instance=pk)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Profile update successful.")
            return HttpResponseRedirect("/profile/")
        else:
            btn="btn-primary"
            return render(request, 'drop_ghor_app/profile.html',{"fm":fm,"btn":btn})


# show user profile

def profile_show(request):
    user=request.user
    pk=Customer.objects.get(user=request.user)
    return render(request,"drop_ghor_app/profile.html",{"pr":True,"cus":pk,"ctn":"btn-primary"})




#  change userpassword
def cus_change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=ChangePassword(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user)
                messages.success(request,"password changed successfully")
                return HttpResponseRedirect("/profile/")
        else:
            form=ChangePassword(user=request.user)
        return render(request, 'drop_ghor_app/changepassword.html',{"fm":form})
    else:
        return HttpResponseRedirect("/login/")
    

# user LOGOUT

def logout(request):
    logout_auth(request)
    return HttpResponseRedirect("/login/")

# product details page 

def product_det(request,idt,p_name):
    try:
        pro=Product.objects.filter(id=idt,name=p_name).first()
        price_and_att=Product_Price_and_attribute.objects.filter(product=pro.id)
        return render(request,"drop_ghor_app/product_details.html",{"pp":price_and_att,"pro":pro})
    except:
        return HttpResponseRedirect("/")


#product add to cart

def add_to_cart(request):
    if request.user.is_authenticated:
        response=HttpResponseRedirect("/product_det/")
        pro_id = request.GET.get("pro_id")
        att_id_and_quentity = request.GET.get("attid").split(",")
        att_id,quentity=tuple(map(int, att_id_and_quentity))
        pro=Product.objects.get(pk=pro_id)
        att=Product_Price_and_attribute.objects.get(pk=att_id)
        price_and_att=Product_Price_and_attribute.objects.filter(product=pro.id).values_list("id",flat=True)
        if int(att_id) in price_and_att:
            key=Afflink_cookie(pro_id=pro_id,pro_name=pro.name,secretkey=SECRET_KEY).cookie_key()
            link=request.COOKIES.get(key)
            if link is not None:
                val=Afflink_cookie().cookie_value_decode(link).split("'~'")[0].split(",")
                if val[1] == pro.name:  
                    aff=Afflink.objects.get(pk=val[0])
                    crt=Cart.objects.filter(user=request.user,product=pro,Pro_price_att=att).values_list("id",flat=True)
                    if crt:
                        cr=Cart.objects.get(pk=crt[0])
                        cr.quantity=cr.quantity+quentity
                        cr.reffer=aff
                        cr.save()
                    else:
                        crt=Cart(user=request.user,product=pro,Pro_price_att=att,quantity=quentity,reffer=aff)
                        crt.save()
                    response.delete_cookie(key)
                else:
                    response.delete_cookie(key)
            else:
                crt=Cart.objects.filter(user=request.user,product=pro,Pro_price_att=att).values_list("id",flat=True)
                if crt:
                   cr=Cart.objects.get(pk=crt[0])
                   cr.quantity=cr.quantity+quentity
                   cr.save()
                else:
                    crt=Cart(user=request.user,product=pro,Pro_price_att=att,quantity=quentity)
                    crt.save()
        else:
            print("false")
        return response
    else:
        return HttpResponseRedirect("/login/")#need to add forwarding systeam


def affi(request):
    pp= Product.objects.all()
    contex={"pp":pp}
    return render(request,"drop_ghor_app/affili.html",contex)


def affinfo(request):
    return render(request,"drop_ghor_app/affinfo.html")


# aff link redirect target url

def redirect_product_page(request,val):
    re=Aff_url_maker().decode_url(val).split("'~'")
    cookie=Afflink_cookie(pro_id=re[0],pro_name=re[1],aff_id=re[2],secretkey=SECRET_KEY)
    key=cookie.cookie_key()
    val=cookie.cookie_value_encode()
    response = HttpResponseRedirect(f"/product_det/{re[0]}/{re[1]}")
    response.set_cookie(key,val)
    return response

def make_afflink(request,pd,pn):
    if request.user.is_authenticated:
        try:
            if request.user.affiliater.appli=="AP":
                af_pro_id=Afflink.objects.filter(affler=request.user.affiliater.id,product=pd)
                if af_pro_id:
                    af=af_pro_id.values_list("id",flat=True)[0]
                    link=Aff_url_maker(pro_id=pd,pro_name=pn,aff_id=af).encode_url()
                    return render(request,"drop_ghor_app/affinfo.html",{"ln":link})
                else:
                    aff=Affiliater.objects.get(user=request.user.id)
                    pro=Product.objects.get(pk=pd)
                    af_pro_id=Afflink.objects.create(affler=aff,product=pro).save()
                    af_pro_id=Afflink.objects.filter(affler=request.user.affiliater.id,product=pd).values_list("id",flat=True)[0]
                    link=Aff_url_maker(pro_id=pd,pro_name=pn,aff_id=af_pro_id).encode_url()
                    return render(request,"drop_ghor_app/affinfo.html",{"ln":link})
            else:
                return HttpResponse("Your affiliate program request is on review mode.so please wait.")
        except:
            return HttpResponse("You don't have any permisson to generate a product link.")
    else:
        return HttpResponseRedirect("/login/")

        
    


