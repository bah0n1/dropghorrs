from aiohttp import request
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drop_ghor_app import views

urlpatterns = [
    path("",views.index,name="index"),
    path("product/",views.product,name="product"),
    path("product_det/<int:idt>/<str:p_name>/",views.product_det,name="product_details"),
    path("cart/",views.add_to_cart,name="add_to_cart"),
    path("login/",views.login_cls.as_view(),name="login"),
    path("logout/",views.logout,name="logout"),
    path("reg/",views.Cus_reg.as_view(),name="registation"),
    path("profile_edit/",views.Profile_View.as_view(),name="profile_edit"),
    path("profile/",views.profile_show,name="profile"),
    path("product/<str:val>/",views.redirect_product_page,name="ref_product"),
    path("product/mk_aff/<int:pd>/<str:pn>",views.make_afflink,name="mk_link"),
    path("changepass/",views.cus_change_password,name="changepassword"),
    path("affi/",views.affi,name="affi"),
    path("affinfo/",views.affinfo,name="affinfo"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)