from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('shop/', include('contact.urls')),
    path('user/', include('customer.urls')),          
    # Api Collection For Ecommerce
    # path('api/user/', include('customer.urls')),  
            
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )