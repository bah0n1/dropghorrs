from django import forms
from django.contrib.auth import models
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.forms import fields
from django.utils.translation import gettext,gettext_lazy as _
from .models import Customer

# validator start from here
def validate_number(value):
    cc=str(value)
    if cc.startswith("+880"):
        pass
    else:
        raise ValidationError("Oops! plz use +880 in your number ")
def validate_check_mail(value): 
    if value.endswith("@gmail.com"):
        pass
    elif value.endswith("@yahoo.com"):
        pass
    else: 
        raise ValidationError("Oops! we only accept Gmail and Yahoo mail. ")
def validate_check_mail_valided(value): 
    if value.endswith("@gmail.com"):
        pass
    elif value.endswith("@yahoo.com"):
        pass
    else: 
        raise ValidationError("Oops! Enter valid email. ")
def validate_email(value):
    try:
        log_cus=User.objects.get(email=value)
    except:
        log_cus=User.objects.filter(email=value)
    if log_cus:
        raise ValidationError("Oops!This email is already exists . ")
    else:
        pass

# Login form
class LoginForm(forms.Form):
    email =forms.CharField(validators=[validate_check_mail_valided],widget=forms.EmailInput(attrs={"class":"form-control"}),required=True)
    password =forms.CharField(label=_("password"),strip=False,widget=forms.PasswordInput(attrs={"autocomplete":"current-password","class":"form-control"}))

# Registation form
class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    email=forms.CharField(required=True,validators=[validate_check_mail,validate_email],widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(required=True,label="Name",widget=forms.TextInput(attrs={"class":"form-control"}),max_length=30)
    number=forms.CharField(validators=[validate_number],required=True,label= _("Mobile number"),max_length=14,min_length=14, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"start with +880"}))
    address=forms.CharField(required=True,max_length=30,widget=forms.TextInput(attrs={"class":"form-control"}))
    city=forms.CharField(required=True,max_length=30,widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model= User
        fields=["first_name","email","password1","password2"]
        labels={"email":"Email"}
        widgets ={"username":forms.TextInput(attrs={"class":"form-control"}),"first_name":forms.TextInput(attrs={"class":"form-control"}),"last_name":forms.TextInput(attrs={"class":"form-control"})}

# change password from


class ChangePassword(PasswordChangeForm):
    old_password=forms.CharField(label= _("Old Password"),widget=forms.PasswordInput(attrs={"class":"form-control","autocomplete":"current-password","autofocus":True}),strip=False)
    new_password1=forms.CharField(label= _("New Password"),widget=forms.PasswordInput(attrs={"class":"form-control","autocomplete":"new-password"}),strip=False,help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label= _("Confirm Password"),widget=forms.PasswordInput(attrs={"class":"form-control","autocomplete":"new-password"},),strip=False)


class Customer_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['number'].required = True
        self.fields['locality'].required = True
        self.fields['city'].required = True
    class Meta:
        model=Customer
        fields=["name","number","locality","city"]
        labels={"name":"First name","number":"Mobile number","locality":"Address"}
        help_text={"number":"start with +88"}
        widgets={"name":forms.TextInput(attrs={"class":"form-control"}),
                "number":forms.TextInput(attrs={"class":"form-control","placeholder":"start with +880"}),
                "locality":forms.TextInput(attrs={"class":"form-control"}),
                "city":forms.TextInput(attrs={"class":"form-control"})}
