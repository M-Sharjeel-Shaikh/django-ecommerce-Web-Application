import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from customer.models import Cart, Customer, Favourite
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status

from store.models import ColorVariant, Product, SizeVariant
from store.views import nav

# Create your views here.
# =========================== Customer Shopping Journey ====================================
def create_cart(request, product_uid):
    if request.method == "POST":
        customer = auth.get_user(request)
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(uid = product_uid)

        if customer and product and quantity and quantity !=0:
            if color and size:
                color_obj = ColorVariant.objects.get(id = color)
                size_obj = SizeVariant.objects.get(id = size)
                cart = Cart.objects.create(user= customer, product= product, color_varient= color_obj, size_varient= size_obj, quantity= quantity)
            else:
                customer = auth.get_user(request)
                cart = Cart.objects.create(user= customer, product= product, quantity= quantity)

            cart.save()

    return redirect('/user/cart')


def cart(request):
    customer = auth.get_user(request)
    cart_detail = Cart.objects.filter(user = customer).all()
    return render(request, "cart.html", context = {"cart_detail": cart_detail})


def remove_cart(request, cart_uid):
    Cart.objects.filter(id = cart_uid).first().delete()
    return redirect("/user/cart")


def add_favourite(request, product_uid):
    user = auth.get_user(request)
    customer= Customer.objects.get(user = user)
    product = Product.objects.filter(uid = product_uid).first()
    Favourite.objects.get_or_create(user= customer, favourite= product)
    return redirect("/user/favourite")


def favourite_user(request):
    customer = auth.get_user(request)
    customer= Customer.objects.get(user = customer)
    favourite_products = Favourite.objects.filter(user = customer).all()
    return render(request, "favourite.html", context = {"total_product": favourite_products})


def remove_favourite(request, favourite_uid):
    Favourite.objects.filter(id = favourite_uid).first().delete()
    return redirect("/user/favourite")
# =========================== End Customer Shopping Journey ================================


# ====================================== Authentication ======================================
# ============= Login User ===================
def login(request):
    
    if request.method != "POST":
        return render(request, "login.html")
    
    username = request.POST['username']
    password = request.POST['password']

    user_obj = User.objects.filter(username = username).first()

    # ============= Check Username Exists Or Not ===========
    if user_obj is None:
        messages.error(request, "Username Do Not Exist Sign Up Here")
        return redirect('/user/signup')

    customer = Customer.objects.filter(user = user_obj).first()

    if customer is None:
        messages.error(request, "Your Email Not verified")
        return redirect('/user/login')

    user = authenticate(request, username = username, password = password)

    if user is not None:
        auth.login(request,user)
        return redirect('/')
    else:
        messages.error(request, "Invalid email or password")
        return redirect('/user/login')



def sign(request):
    if request.user.is_authenticated:   
        return render(request, "index.html")

    if request.method != 'POST':
        return render(request, "register.html")
    
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    try:            
        # =========== Check Username is available ===============
        if User.objects.filter(username = username).first():
            return render(request,"register.html", {'error': "User Name alraedy exist"}) 

        # =========== Check Email is available ===============
        if User.objects.filter(email = email).first():
            return render(request,"register.html", {'error': "Email Address alraedy exist"})  

        # =========== Check Password are Match ===============
        if password != confirm_password:
            return render(request,"register.html", {'error': "Password Not Match"})           

        user_obj = User.objects.create(username = username, email = email)
        user_obj.set_password(password)
        user_obj.save()

        auth_token = str(uuid.uuid4())
        customer = Customer.objects.create(user = user_obj, auth_token = auth_token)
        customer.save()

        send_email(email, auth_token)
        messages.success(request, "Token Sent")
        messages.success(request, "Token is Sent to your email address and check your mail")
        return redirect('/user/token')

    except Exception as e:
        print(e)
        return render(request, "error.html", {'error': "There is something Wroung Try Again"} )



# =========== Email For Forget Password =============
def forget(request):
    if request.user.is_authenticated:   
        return render(request, "index.html")
    
    if request.method == 'POST':
        try:
            email = request.POST['email']

            # ============ checking email Exists or not ===========
            if not User.objects.filter(email = email).first():
                return render(request,"register.html", {'error': "User Do not Exists Please Sign Up Here"})      

            user_obj = User.objects.get(email = email)
            auth_token = str(uuid.uuid4())
            customer = Customer.objects.update(auth_token = auth_token)
            send_email_forget_password(email, auth_token)
            messages.success(request, "Token is sent to your Email ")
            return render(request,"token.html")

        except Exception as e:
            print(e)
            return render(request,"error.html",{'error': "There is something wroung"})

    elif request.method == 'GET':
        return render(request, "forget.html")
    else:
        return render(request, "index.html")



# =========== Send Email With Uuid token ============
def send_email(email, auth_token):
    subject="your token is verifies"
    message=f'Hi User, Click link to verify your account http://127.0.0.1:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [email]

    send_mail(subject,message, email_from,recepient_list)


# =========== Forget Password =======================
def change_password(request, auth_token):
    if request.user.is_authenticated:   
        return render(request, "index.html")

    context = {} 

    try:
        customer_obj = Customer.objects.filter(auth_token = auth_token).first()
        messages.success(request, "Now You can change your password")
        
        context = { 'user_id': customer_obj.user.id }
        # ============ Reset New password here =============
        if request.method == "POST":
            new_password = request.POST['new_password']
            match_password = request.POST['confirm_password']
            user_id = request.POST.get('user_id')

            # ============ User Id Dont Exist =============
            if user_id is None:
                messages.info(request, "No user id Found")
                return redirect(f'/user/change_password/{auth_token}')
            
            # ============== Password not Match ================
            if new_password != match_password:
                messages.success(request, "Password Not Match")
                return redirect('/user/change_password')
        
        elif request.method == 'GET':
            return render(request, "change_password.html")
        else:
            return render(request, "index.html")
        
        user_obj = User.objects.get(id= user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('/user/login')

    except Exception as e:
        print(e)
        return render(request,"error.html", {'error' : "Something went Wroung"})
    
    

def token(request):
    if request.user.is_authenticated:   
        return render(request, "index.html")
    
    messages.success(request, "Validation Email is sent to you, Check your mail")
    return render(request, "token.html")
  


def error(request):
    if request.user.is_authenticated:   
        return render(request, "index.html")
    return render(request, "error.html")



# =========== Verify User Uuid token =================
def verify(request, auth_token):
    if request.user.is_authenticated:   
        return render(request, "index.html")
    try:
        customer = Customer.objects.filter(auth_token = auth_token).first()

        if not customer:
            return render(request,"error.html", {'error': "Not Valid Customer"})
        
        customer.is_verified = True
        customer.save()
        messages.success(request, "Email is verified")
        print("Email is verified")
        print("Email is verified")
        return redirect('/user/login')
    except Exception as e:
        print(e)
        return redirect("/user/error")


# =========== Send Email With Uuid token =============
def send_email_forget_password(email, auth_token):
    subject="Reset Account Password"
    message=f'Hi User, Click link to Reset your password http://127.0.0.1:8000/change_password/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [email]

    send_mail(subject,message, email_from,recepient_list)


# =========================== API Authentication =================================
def Apilogin(request):
    return Response(status=status.HTTP_201_CREATED)




