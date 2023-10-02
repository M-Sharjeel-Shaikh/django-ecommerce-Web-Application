from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from contact.models import Contact

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
        messages.success(request, 'Fill all required Fields')
        return render(request, "error.html")
        