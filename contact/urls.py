from django.urls import path
from .views import contact, ApiContact

urlpatterns = [
    path('contact/', contact, name="contact"),
    path('api/contact/', ApiContact, name="api-contact"),
    ]