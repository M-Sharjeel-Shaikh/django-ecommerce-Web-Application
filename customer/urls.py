from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # =========== Customer Urls ============
    path('forget/', forget, name="forget"),
    path('email_validate/', send_email, name="email_validate"),
    path('login/', login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('token', token, name='token'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error/',error, name='error'),
    path('signup/', sign, name="sign"),
    path('change_password/<auth_token>', change_password, name="change_password"), 

    # =========== Customer Journey ==========
    path('cart/', cart, name='cart'),
    path('create_cart/<product_uid>', create_cart, name='create_cart'),
    path('remove_cart/<cart_uid>', remove_cart, name='remove-cart'),
    path('favourite/', favourite_user, name='favourite'),
    path('favourite/<product_uid>', add_favourite, name='add_favourite'),
    path('remove_favourite/<favourite_uid>', remove_favourite, name='remove-favourite'),

    # =========== Customer Urls for APIs=====
    path('Login/', Apilogin, name="Login"),
    # path('Login/', login, name="login"),
    ]