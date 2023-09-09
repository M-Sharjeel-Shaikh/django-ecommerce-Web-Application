from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from customer.models import *
from store.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import auth
# from django.template.response import TemplateResponse


# ====== filter price one not working

# Create your views here.
# def average(slug):
#     product = Product.objects.get(slug = slug)
#     reviews = User_Review.objects.filter(product__slug=slug).order_by("-comment")
#     average = User_Review.aggregate(Avg("rate"))["rate__avg"]

#     if average == None:
#         average=0
#     else:
#         average = round(average,2)

#         context={
#             "product":product,
#             "reviews":reviews,
#             "average":average,
#         }
#     print(product)
#     print(reviews)
#     print(average)

#     return product, reviews, average

    # ======= Favourite =================
    # customer = request.user.id
    # print("================= ", customer)
    # color = Favourite.objects.filter(id = customer)


def home(request):
    men_total_product = Product.objects.filter(category = "1").count()
    womenmen_total_product = Product.objects.filter(category = "2").count()
    kid_total_product = Product.objects.filter(category = "3").count()
    shirt_total_product = Product.objects.filter(category = "4").count()
    jeans_total_product = Product.objects.filter(category = "5").count()
    furniture_total_product = Product.objects.filter(category = "6").count()
    digital_total_product = Product.objects.filter(category = "7").count()
    watch_total_product = Product.objects.filter(category = "8").count()
    household_total_product = Product.objects.filter(category = "9").count()
    cosmetic_total_product = Product.objects.filter(category = "10").count()
    jacket_total_product = Product.objects.filter(category = "11").count()
    shoes_total_product = Product.objects.filter(category = "12").count()

    # ================= Feature Products ==========================
    feature_product = Product.objects.all()[:8]

    reviews = Review.objects.all()
    average = reviews.aggregate(Avg("rate"))["rate__avg"]

    average = 0 if average is None else round(average,2)

    context={
        'men': men_total_product,
        'women':womenmen_total_product,
        'kid':kid_total_product,
        'shirt':shirt_total_product,
        'jeans':jeans_total_product,
        'furniture':furniture_total_product,
        'digital':digital_total_product,
        'watch':watch_total_product,
        'household':household_total_product,
        'cosmetic':cosmetic_total_product,
        'jacket':jacket_total_product,
        'shoes':shoes_total_product,
        'feature_product' : feature_product,
        'average':average
    }
    return render(request, "index.html",context)


def nav(request):
    try:
        customer = auth.get_user(request)
        count = Cart.objects.filter(user = customer).count()
        return render(request, "nav.html", context={'cart_count': count})
    except Exception as e:
        print(e)
        return redirect('/')



def checkout(request):
    return render(request, "checkout.html")



def comment(request, uid):
    try:
        if request.method != "POST":
            return redirect('/shop')
        
        user = auth.get_user(request)
        customer = Customer.objects.get(user= user)
        message = request.POST['message']
        product = Product.objects.get(uid = uid)
        review = Review.objects.create(user = customer, product = product, comment = message)
        review.save()
        return detail(request, uid)

    except Exception as e:
        print(e)
        return HttpResponse("someThing Wroung ", e)



def detail(request, uid):
    try:
        product = Product.objects.get(uid = uid)
        sizes_variant = product.size_variant.all()
        color_variant = product.color_variant.all()
        reviews = Review.objects.filter(product__uid=uid).order_by("-created_at")[:5]

        # average=0
        # if reviews:
        #     average = reviews.aggregate(Avg("rate"))["rate__avg"]

        # average = 0 if average is None else round(average,2)

        context={
            "product":product,
            "reviews":reviews,
            # "average":average,
            "sizes" : sizes_variant,
            "colors" : color_variant,
        }

        return render(request, "detail.html", context)
    except Exception as e:
        print(e)
        return render(request, "shop.html")



def shop(request):
    total_no_product = Product.objects.all().count()

    # =========== Shop Data unfilter ============
    shop_products = Product.objects.all().order_by('-rating')

    paginator=Paginator(shop_products,6)
    page_number=request.GET.get('page')
    # ======= which connect page connect and pagination =======
    page_data=paginator.get_page(page_number)
    total=page_data.paginator.num_pages

    context = {
        'shop_product':page_data,
        'totalpage':[n+1 for n in range(total)],
        'total_no_product' : total_no_product,
    }

    return render(request, "shop.html", context)


# =========================== Search Query ==================================
def search(request):
    search_query = request.GET.get('search')
    if search_query == "":
        return redirect('/shop')

    result = Product.objects.filter(name__icontains=search_query).order_by('-rating')[:10]

    if not result:
        messages.info(request, "No Data Found")
        return render(request, "query.html")
    
    return render(request, "query.html", context={"total_product": result})

# =========================== END Search Query ==============================


# =========================== Favourite & Cart ==============================
def favourite(request, slug=None):
    try:
        if not slug:
            user = request.user
            customer = Customer.objects.get(user=user)
            products = Customer.objects.filter(user = customer).all()
            context ={
                'total_product': products,
            }
            return render(request, 'favourite.html', context)
        
        try: 
            if slug:
                user = request.user
                product = Product.objects.get(slug=slug)
                my_cus = Customer.objects.get(user=user)
                print(my_cus)
                # favourite_instance.user = my_cus
                favourite = Favourite.objects.create(user=my_cus, favourite=product).save()
                print("congrate ========================", favourite)
                return redirect('/')
            
        except Exception as e:
            print("======================= ",e)
            return redirect('/contact')

    except Exception as e:
        print(e)
        return redirect('/')




# =========================== End Favourite & Cart ===========================


# =========================== Category Views =================================

def men(request):
    try:
        # show_no_product = request.GET['show_no_product', 10]
        men_product = Product.objects.filter(category = "1").order_by('-rating')

        paginator=Paginator(men_product,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : men_product,
            'url': 'men/dresses',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def women(request):
    try:
        women_product = Product.objects.filter(category = "2").order_by('-rating')
        
        paginator=Paginator(women_product,2)
        page_number=request.GET.get('page')
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : women_product,
            'url': 'women/dresses',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def kid(request):
    try:
        kid_product = Product.objects.filter(category = "3").order_by('-rating')
        
        paginator=Paginator(kid_product,2)
        page_number=request.GET.get('page')
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : kid_product,
            'url': 'kid/dresses',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print("==================== Exception ==================")
        print(e)
        return render(request, "shop.html")


def shirt(request):
    try:
        # show_no_product = request.GET['show_no_product', 10]
        shirt_product = Product.objects.filter(category = "4").order_by('-rating')

        paginator=Paginator(shirt_product,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : shirt_product,
            'url': 'shirt/dresses',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def jeans(request):
    try:
        # show_no_product = request.GET['show_no_product', 10]
        jeans_product = Product.objects.filter(category = "5").order_by('-rating')

        paginator=Paginator(jeans_product,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : jeans_product,
            'url': 'jeans/dresses',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def furniture(request):
    try:
        # show_no_product = request.GET['show_no_product', 10]
        furniture_product = Product.objects.filter(category = "6").order_by('-rating')

        paginator=Paginator(furniture_product,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : furniture_product,
            'url': 'furniture/products',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def digital(request):
    try:
        # show_no_product = request.GET['show_no_product', 10]
        digital_product = Product.objects.filter(category = "7").order_by('-rating')

        paginator=Paginator(digital_product,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : digital_product,
            'url': 'digital/products',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def watch(request):
    try:
        # show_no_product = request.GET['show_no_product', 10]
        watch_product = Product.objects.filter(category = "8").order_by('-rating')

        paginator=Paginator(watch_product,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : watch_product,
            'url': 'watch/products',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def household(request):
    try:
        household_product = Product.objects.filter(category = "9").order_by('-rating')

        paginator=Paginator(household_product,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : household_product,
            'url': 'household/products',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def cosmetic(request):
    try:
        cosmetic_product = Product.objects.filter(category = "10").order_by('-rating')

        paginator=Paginator(cosmetic_product,1)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : cosmetic_product,
            'url': 'cosmetic/products',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def jacket(request):
    try:
        jacket_product = Product.objects.filter(category = "11").order_by('-rating')

        paginator=Paginator(jacket_product,1)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : jacket_product,
            'url': 'jacket/products',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


def shoes(request):
    try:
        shoes_product = Product.objects.filter(category = "12").order_by('-rating')

        paginator=Paginator(shoes_product,1)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            # "select_category" : shoes_product,
            'url': 'shoes/products',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
        }
        return render(request, "shop.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")
# =========================== End Category Views =============================
