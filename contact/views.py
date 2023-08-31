from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from contact.models import Contact
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ContactSerializer
from rest_framework.response import Response

# Create your views here.
def contact(request):
    try:
        if request.method != "POST":
            return render(request, "contact.html")

        if request.POST['email'] and request.POST['message']:
            name = request.POST['name']
            subject = request.POST['subject']
            email = request.POST['email']
            message = request.POST['message']
            contact = Contact.objects.create(name=name, email=email, subject=subject, message=message)
            contact.save()
            messages.success(request, 'Your message is received to our team and we will contact back you soon')
        else:
            messages.success(request, 'Fill all required Fields')

        return redirect('/shop/contact')
    
    except Exception as e:      
        return HttpResponse("there is something wroung", e)


@api_view(['POST'])
def ApiContact(request):
    contact = ContactSerializer(data=request.data)

    if contact.is_valid():
        contact.save()
        content = {'message': 'contact is created'}
        return Response(content, status=status.HTTP_201_CREATED)
    else:
        return Response(status=400)
        