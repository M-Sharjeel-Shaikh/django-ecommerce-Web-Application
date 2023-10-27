from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from customer.models import *
from store.models import *
from django.contrib import messages
from django.db.models import Avg
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from store.util import shop_pagination
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
    men_total_product = Product.objects.filter(category="1").count()
    womenmen_total_product = Product.objects.filter(category="2").count()
    kid_total_product = Product.objects.filter(category="3").count()
    shirt_total_product = Product.objects.filter(category="4").count()
    jeans_total_product = Product.objects.filter(category="5").count()
    furniture_total_product = Product.objects.filter(category="6").count()
    digital_total_product = Product.objects.filter(category="7").count()
    watch_total_product = Product.objects.filter(category="8").count()
    household_total_product = Product.objects.filter(category="9").count()
    cosmetic_total_product = Product.objects.filter(category="10").count()
    jacket_total_product = Product.objects.filter(category="11").count()
    shoes_total_product = Product.objects.filter(category="12").count()

    # ================= Feature Products ==========================
    feature_product = Product.objects.all()[:8]

    reviews = Review.objects.all()
    average = reviews.aggregate(Avg("rate"))["rate__avg"]

    average = 0 if average is None else round(average, 2)

    context = {
        'men': men_total_product,
        'women': womenmen_total_product,
        'kid': kid_total_product,
        'shirt': shirt_total_product,
        'jeans': jeans_total_product,
        'furniture': furniture_total_product,
        'digital': digital_total_product,
        'watch': watch_total_product,
        'household': household_total_product,
        'cosmetic': cosmetic_total_product,
        'jacket': jacket_total_product,
        'shoes': shoes_total_product,
        'feature_product': feature_product,
        'average': average
    }
    return render(request, "index.html", context)


def nav(request):
    try:
        customer = auth.get_user(request)
        count = Cart.objects.filter(user=customer).count()
        return render(request, "nav.html", context={'cart_count': count})
    except Exception as e:
        print(e)
        return redirect('/')


@login_required
def comment(request, uid):
    try:
        if request.method != "POST":
            return redirect('/shop')

        user = auth.get_user(request)
        customer = Customer.objects.get(user=user)
        message = request.POST.get('message')
        product = Product.objects.get(uid=uid)
        review = Review.objects.create(
            user=customer, product=product, comment=message)
        review.save()
        return detail(request, uid)

    except Exception as e:
        print(e)
        return HttpResponse("someThing Wroung ", e)


@login_required
def detail(request, uid):
    try:
        product = Product.objects.get(uid=uid)
        sizes_variant = product.size_variant.all()
        color_variant = product.color_variant.all()
        reviews = Review.objects.filter(product__uid=uid).order_by("-created_at")[:5]

        # average=0
        # if reviews:
        #     average = reviews.aggregate(Avg("rate"))["rate__avg"]

        # average = 0 if average is None else round(average,2)

        context = {
            "product": product,
            "reviews": reviews,
            # "average":average,
            "sizes": sizes_variant,
            "colors": color_variant,
        }

        return render(request, "detail.html", context)
    except Exception as e:
        print(e)
        return render(request, "error.html")


@login_required
def shop(request):
    shop_products = Product.objects.all().order_by('-rating')
    context = shop_pagination(request, shop_products)
    total_no_product = shop_products.count()
    context['response'] = shop_products
    context['total_no_product'] = total_no_product
    return render(request, "shop.html", context)



# =========================== Search Query ==================================
def search(request):
    search_query = request.GET.get('query', '')
    result_query = Product.objects.filter(name__icontains=search_query).order_by('-rating')[:100]
    context = shop_pagination(request, result_query)
    return render(request, "query.html", context)


# =========================== END Search Query ==============================


# =========================== Favourite & Cart ==============================
@login_required
def favourite(request, slug=None):
    try:
        if not slug or slug is None:
            user = request.user
            customer = Customer.objects.get(user=user)
            products = Customer.objects.filter(user=customer).all()
            context = {
                'total_product': products,
            }
            return render(request, 'favourite.html', context)

        try:
            if slug:
                user = request.user
                product = Product.objects.get(slug=slug)
                my_cus = Customer.objects.get(user=user)
                favourite = Favourite.objects.create(
                    user=my_cus, favourite=product).save()
                return redirect('/')

        except Exception as e:
            print("======================= ", e)
            return redirect('/contact')

    except Exception as e:
        print(e)
        return redirect('/')

# =========================== End Favourite & Cart ==========================


# =========================== Category Views ================================
@login_required
def men(request):
    try:
        men_product = Product.objects.filter(category="1").order_by('-rating')
        context = shop_pagination(request, men_product)
        context['url'] = 'men/dresses'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def women(request):
    try:
        women_product = Product.objects.filter(category="2").order_by('-rating')
        context = shop_pagination(request, women_product)
        context['url'] = 'women/dresses'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def kid(request):
    try:
        kid_product = Product.objects.filter(category="3").order_by('-rating')
        context = shop_pagination(request, kid_product)
        context['url'] = 'kid/dresses'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def shirt(request):
    try:
        shirt_product = Product.objects.filter(category="4").order_by('-rating')
        context = shop_pagination(request, shirt_product)
        context['url'] = 'shirt/dresses'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def jeans(request):
    try:
        jeans_product = Product.objects.filter(category="5").order_by('-rating')
        context = shop_pagination(request, jeans_product)
        context['url'] = 'jeans/dresses'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def furniture(request):
    try:
        furniture_product = Product.objects.filter( category="6").order_by('-rating')
        context = shop_pagination(request, furniture_product)
        context['url'] = 'furniture/products'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def digital(request):
    try:
        digital_product = Product.objects.filter(category="7").order_by('-rating')
        context = shop_pagination(request, digital_product)
        context['url'] = 'digital/products'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def watch(request):
    try:
        # show_no_product = request.GET['show_no_product', 10]
        watch_product = Product.objects.filter(category="8").order_by('-rating')
        context = shop_pagination(request, watch_product)
        context['url'] = 'watch/products'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def household(request):
    try:
        household_product = Product.objects.filter(category="9").order_by('-rating')
        context = shop_pagination(request, household_product)
        context['url'] = 'household/products'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def cosmetic(request):
    try:
        cosmetic_product = Product.objects.filter(category="10").order_by('-rating')
        context = shop_pagination(request, cosmetic_product)
        context['url'] = 'cosmetic/products'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def jacket(request):
    try:
        jacket_product = Product.objects.filter(category="11").order_by('-rating')
        context = shop_pagination(request, jacket_product)
        context['url'] = 'jacket/products'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")


@login_required
def shoes(request):
    try:
        shoes_product = Product.objects.filter(category="12").order_by('-rating')
        context = shop_pagination(request, shoes_product)
        context['url'] = 'shoes/products'
        return render(request, "category.html", context)
    except Exception as e:
        print(e)
        return render(request, "index.html")
# =========================== End Category Views =============================
