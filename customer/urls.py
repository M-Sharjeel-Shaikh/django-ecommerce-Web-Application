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
    path('cart/<product_uid>', create_cart, name='cart'),

    # =========== Customer Urls for APIs=====
    path('Login/', Apilogin, name="Login"),
    # path('Login/', login, name="login"),
    ]