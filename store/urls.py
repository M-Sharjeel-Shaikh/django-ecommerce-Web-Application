from django.urls import path
from django.views.generic import TemplateView
from . views import *

urlpatterns = [
    path('', home, name='home'),
    path('nav/', nav, name="nav"),
    path('detail/<uid>', detail, name="detail"),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('query/', TemplateView.as_view(template_name='query.html'), name='query'),
    path('error/', TemplateView.as_view(template_name='error.html'), name='error'),
    path('search/', search, name="search"),
    path('comment/<uid>', comment, name="comment"),
    path('shop/', shop, name="shop"),

    #=============== filtering shop ==================

    # ================== favourite & Cart ===================
    path('product/favourite/', favourite, name="favourite"),
    path('favourite/<slug:slug>/', favourite, name="add_favourite"),
    
    #=============== product ==================
    path('men/dresses/', men, name="men"),
    path('women/dresses/', women, name="women"),
    path('kid/dresses/', kid, name="kid"),
    path('shirt/dresses/', shirt, name="shirt"),
    path('jeans/dresses/', jeans, name="jeans"),
    path('furniture/products/', furniture, name="furniture"),
    path('digital/products/', digital, name="digital"),
    path('watch/products/', watch, name="watch"),
    path('household/products/', household, name="household"),
    path('cosmetic/products/', cosmetic, name="cosmetic"),
    path('jacket/products/', jacket, name="jacket"),
    path('shoes/products/', shoes, name="shoes"),
    ]