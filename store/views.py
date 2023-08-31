from django.shortcuts import render, redirect
from django.http import HttpResponse
from customer.models import *
from store.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import auth


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
        cart_detail = Cart.objects.filter(user = customer).all()
        total_cart = cart_detail.count()

        context= {
            "total_cart": total_cart
        }
        return HttpResponse(context)
    except Exception as e:
        print(e)
        return redirect('/')



def checkout(request):
    return render(request, "checkout.html")



def comment(request, slug):
    try:
        if request.method == "POST":
            user = request.user.id
            print("user id: " )
            print(user)
            msg = request.POST['message']
            username = request.POST['username']
            product = Product.objects.get(slug=slug)
            print("product name:  " )
            print(product)
            
            if user:
                user = Customer.objects.filter(id = user)
                print("---------------------------------------------------",user)
                

            # if star1 or star2 or star3 or star4 or star5:
            # star1 = request.POST['start1']
            # print(star1)
                # star2 = request.POST['start2']
                # star3 = request.POST['start3']
                # star4 = request.POST['start4']
                # star5 = request.POST['start5']
                # star_list=[star1,star2,star3,star4,star5]

                # print("################")
                # star = max(star_list)
            
            reviews = Review.objects.create(
                user = product,
                # rate = star,
                rate = 3,
                product = user,
                comment = msg,
            )
            print("################")
            print(reviews)
            print("################")
            reviews.save()
            return redirect('/checkout')
        else:
            return redirect('/shop')
    except Exception as e:
        print(e)
        return HttpResponse("someThing Wroung ")



def detail(request, uid):
    # try:
    product = Product.objects.get(uid = uid)
    sizes_variant = product.size_variant.all()
    color_variant = product.color_variant.all()
    # reviews = Review.objects.filter(product__slug=slug).order_by("-comment")
    # average=0
    # if reviews:
    #     average = reviews.aggregate(Avg("rate"))["rate__avg"]

    # average = 0 if average is None else round(average,2)

    context={
        "product":product,
        # "reviews":reviews,
        # "average":average,
        "sizes" : sizes_variant,
        "colors" : color_variant,
    }

    return render(request, "detail.html", context)
    # except Exception as e:
    #     print(e)
    #     return render(request, "shop.html")



def shop(request):
    # query_context=[]
    context = []
    total_no_product = Product.objects.all().count()

    # if 'price_form' in request.GET:
    #     # try:
    #     one = request.GET.get('price_range_first')
    #     two = request.GET.get('price_range_second')
    #     three = request.GET.get('price_range_third')
    #     four = request.GET.get('price_range_fourth')
    #     five = request.GET.get('price_range_fifth')

    #     if one:
    #         products = Product.objects.filter( (Q(price__lte = 100) & Q(price__gte = 0)) & (Q(discount_price__gte = 0) & Q(discount_price__lte = 100) | Q(discount_price = 0)) ).order_by('-rating')
    #         print("======================",products)
    #         first_range_no_product = products.count()
            
    #         paginator=Paginator(products,6)
    #         page_number=request.GET.get('page')
    #         # ======= which connect page connect and pagination =======
    #         page_data=paginator.get_page(page_number)
    #         total=page_data.paginator.num_pages

    #         context = {
    #             'url': 'shop',
    #             'total_product':page_data,
    #             'totalpage':[n+1 for n in range(total)],
    #             'total_no_product' : total_no_product,          
    #             'first_range_no_product':first_range_no_product,
    #         }
    #         return render(request, "shop.html", context)

    #     if two:
    #         products = Product.objects.filter( (Q(price__lte = 200) & Q(price__gte = 100)) & (Q(discount_price__gte = 100) & Q(discount_price__lte = 200) | Q(discount_price = 0)) ).order_by('-rating')
    #         second_range_no_product = products.count()
    #         context.append({
    #             'total_product': products,
    #             'second_range_no_product': second_range_no_product
    #         })
     
        
    #     if three:
    #         products = Product.objects.filter( Q(price__lte = 300) & Q(price__gte = 200) & (Q(discount_price__gte = 200) & Q(discount_price__lte = 300) | Q(discount_price = 0)) ).order_by('-rating')
    #         third_range_no_product = products.count()
    #         context.append({
    #             'total_product': products,
    #             'third_range_no_product':third_range_no_product,
    #         })
      

    #     if four:
    #         products = Product.objects.filter( (Q(price__lte = 400) & Q(price__gte = 300)) & (Q(discount_price__gte = 300) & Q(discount_price__lte = 400) | Q(discount_price = 0)) ).order_by('-rating')
    #         fourth_range_no_product = products.count()
    #         context.append({
    #             'total_product': products,
    #             'fourth_range_no_product': fourth_range_no_product,
    #         })


    #     if five:
            # products = Product.objects.filter( Q(price__lte = 500) & Q(price__gte = 400) & ( Q(discount_price__gte = 400) & Q(discount_price__lte = 500) | Q(discount_price = 0) )  ).order_by('-rating')
            # fifth_range_no_product = products.count()

            # paginator=Paginator(products,6)
            # page_number=request.GET.get('page')
            # # ======= which connect page connect and pagination =======
            # page_data=paginator.get_page(page_number)
            # total=page_data.paginator.num_pages

            # context = {
            #     'url': 'shop',
            #     'total_product':page_data,
            #     'totalpage':[n+1 for n in range(total)],
            #     'total_no_product' : total_no_product,          
            #     'fifth_range_no_product':fifth_range_no_product,
            # }
            # return render(request, "shop.html", context)


    # paginator=Paginator(products,6)
    # page_number=request.GET.get('page')
    # # ======= which connect page connect and pagination =======
    # page_data=paginator.get_page(page_number)
    # total=page_data.paginator.num_pages

    # context = {
    #     'url': 'shop',
    #     'total_product':page_data,
    #     'totalpage':[n+1 for n in range(total)],
    #     'total_no_product' : total_no_product,          
    #     'fifth_range_no_product':fifth_range_no_product,
    # }
    # return render(request, "shop.html", context)
    
        # except Exception as e:
        #     print(e)
        #     return redirect("/contact")


    # if 'color_form' in request.GET:
    #     try:
    #         black_color = request.GET.get('Black')
    #         White_color = request.GET.get('White')
    #         red_color = request.GET.get('Red')
    #         blue_color = request.GET.get('Blue')
    #         green_color = request.GET.get('Green')

    #         # # product = Product.objects.all()
    #         # black_color_id = ColorVariant.objects.get(color_name= "Black")
    #         # black_color_id = ColorVariant.objects.get(color_name= "Black")
    #         # black_color_id = ColorVariant.objects.get(color_name= "Black")
    #         # black_color_id = ColorVariant.objects.get(color_name= "Black")
    #         # print("======== color id", black_color_id)
    #         # black = Product.objects.filter(color_variant = black_color_id)
                
    #         # print("===== Black", black)
            
    #         if black_color:
    #             black_color_id = ColorVariant.objects.get(color_name= "Black")
    #             black = Product.objects.filter(color_variant = black_color_id)
    #             total= black.count()
    #             context = {
    #                 'total_product': black,
    #                 'total_black_products': total,
    #             }
    #             return render(request, "shop.html", context)
            

    #         if White_color:
    #             white_color_id = ColorVariant.objects.get(color_name= "White")
    #             white = Product.objects.filter(color_variant = white_color_id)
    #             total= white.count()
    #             context = {
    #                 'total_product': white,
    #                 'total_white_products': total,
    #             }
    #             return render(request, "shop.html", context)
            

    #         if red_color:
    #             red_color_id = ColorVariant.objects.get(color_name= "Red")
    #             red = Product.objects.filter(color_variant = red_color_id)
    #             total= red.count()
    #             context = {
    #                 'total_product': red,
    #                 'total_red_products': total,
    #             }
    #             return render(request, "shop.html", context)
            

    #         if blue_color:
    #             blue_color_id = ColorVariant.objects.get(color_name= "Blue")
    #             blue = Product.objects.filter(color_variant = blue_color_id)
    #             total= blue.count()
    #             context = {
    #                 'total_product': blue,
    #                 'total_blue_products': total,
    #             }
    #             return render(request, "shop.html", context)
            

    #         if green_color:
    #             green_color_id = ColorVariant.objects.get(color_name= "Green")
    #             green = Product.objects.filter(color_variant = green_color_id)
    #             total= green.count()
    #             context = {
    #                 'total_product': green,
    #                 'total_green_products': total,
    #             }
    #             return render(request, "shop.html", context)

    #     except Exception as e:
    #         print(e)
    #         return redirect("/shop")


    # if 'size_form' in request.GET:
    #     try:
    #         size_x_small = request.GET.get('XS')
    #         size_small = request.GET.get('S')
    #         size_medium = request.GET.get('M')
    #         size_large = request.GET.get('L')
    #         size_x_large = request.GET.get('XL')

    #         if size_x_small:
    #             xs_size_id = SizeVariant.objects.get(size_name = "XS")
    #             xs_size = Product.objects.filter(size_variant = xs_size_id) 
    #             total= xs_size.count()           
    
    #             context = {
    #                 'total_product': xs_size,
    #                 'total_xs_products': total,
    #             }
    #             return render(request, "shop.html", context)


    #         if size_small:
    #             small_size_id = SizeVariant.objects.get(size_name = "S")
    #             s_size = Product.objects.filter(size_variant = small_size_id) 
    #             total= s_size.count()           
    
    #             context = {
    #                 'total_product': s_size,
    #                 'total_small_products': total,
    #             }
    #             return render(request, "shop.html", context)


    #         if size_medium:
    #             m_size_id = SizeVariant.objects.get(size_name = "M")
    #             m_size = Product.objects.filter(size_variant = m_size_id) 
    #             total= m_size.count()           
    
    #             context = {
    #                 'total_product': m_size,
    #                 'total_medium_products': total,
    #             }
    #             return render(request, "shop.html", context)


    #         if size_large:
    #             l_size_id = SizeVariant.objects.get(size_name = "L")
    #             l_size = Product.objects.filter(size_variant = l_size_id) 
    #             total= l_size.count()           
    
    #             context = {
    #                 'total_product': l_size,
    #                 'total_large_products': total,
    #             }
    #             return render(request, "shop.html", context)


    #         if size_x_large:
    #             xl_size_id = SizeVariant.objects.get(size_name = "XL")
    #             xl_size = Product.objects.filter(size_variant = xl_size_id) 
    #             total= xl_size.count()           
    
    #             context = {
    #                 'total_product': xl_size,
    #                 'total_xlarge_products': total,
    #             }
    #             return render(request, "shop.html", context)

    #     except Exception as e:
    #         print(e)
    #         return redirect('/shop')


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


# ======== Search Query =========
def search(request):
    search_query = request.GET.get('search')
    if search_query == "":
        return redirect('/shop')

    result = Product.objects.filter(name__icontains=search_query).order_by('-rating')[:10]

    if not result:
        messages.info(request, "No Data Found")
        return render(request, "query.html")
    
    return render(request, "query.html", context={"total_product": result})
 

# =========================== Filter Option =================================
def price_filter(request):
    # try:
    total_no_product = Product.objects.all().count()

    one = request.GET.get('price_range_first')
    two = request.GET.get('price_range_second')
    three = request.GET.get('price_range_third')
    four = request.GET.get('price_range_fourth')
    five = request.GET.get('price_range_fifth')

    if one:
        total_products = Product.objects.filter( (Q(price__lte = 100) & Q(price__gte = 0)) & (Q(discount_price__gte = 0) & Q(discount_price__lte = 100) | Q(discount_price = 0)) ).order_by('-rating')
        first_range_no_product = total_products.count()
        
        paginator=Paginator(total_products,2)
        page_number=request.GET.get('page')
        # ======= which connect page connect and pagination =======
        page_data=paginator.get_page(page_number)
        total=page_data.paginator.num_pages

        context = {
            'url':'price_filter/?price_range_first=on',
            'total_product':page_data,
            'totalpage':[n+1 for n in range(total)],
            'first_range_no_product':first_range_no_product,
            'total_no_product' : total_no_product,
        }
        return render(request, "shop.html", context)


        # if two:
        #     products = Product.objects.filter( (Q(price__lte = 200) & Q(price__gte = 100)) & (Q(discount_price__gte = 100) & Q(discount_price__lte = 200) | Q(discount_price = 0)) ).order_by('-rating')
        #     second_range_no_product = products.count()
        #     context.append({
        #         'total_product': products,
        #         'second_range_no_product': second_range_no_product
        #     })
        
        
        # if three:
        #     products = Product.objects.filter( Q(price__lte = 300) & Q(price__gte = 200) & (Q(discount_price__gte = 200) & Q(discount_price__lte = 300) | Q(discount_price = 0)) ).order_by('-rating')
        #     third_range_no_product = products.count()
        #     context.append({
        #         'total_product': products,
        #         'third_range_no_product':third_range_no_product,
        #     })
        

        # if four:
        #     products = Product.objects.filter( (Q(price__lte = 400) & Q(price__gte = 300)) & (Q(discount_price__gte = 300) & Q(discount_price__lte = 400) | Q(discount_price = 0)) ).order_by('-rating')
        #     fourth_range_no_product = products.count()
        #     context.append({
        #         'total_product': products,
        #         'fourth_range_no_product': fourth_range_no_product,
        #     })


        # if five:
            # products = Product.objects.filter( Q(price__lte = 500) & Q(price__gte = 400) & ( Q(discount_price__gte = 400) & Q(discount_price__lte = 500) | Q(discount_price = 0) )  ).order_by('-rating')
            # fifth_range_no_product = products.count()

            # paginator=Paginator(products,6)
            # page_number=request.GET.get('page')
            # # ======= which connect page connect and pagination =======
            # page_data=paginator.get_page(page_number)
            # total=page_data.paginator.num_pages

            # context = {
            #     'url': 'shop',
            #     'total_product':page_data,
            #     'totalpage':[n+1 for n in range(total)],
            #     'total_no_product' : total_no_product,          
            #     'fifth_range_no_product':fifth_range_no_product,
            # }
            # return render(request, "shop.html", context)

    return redirect('/shop')


    # except Exception as e:
    #     print("======= error: ",e)
    #     return redirect('/contact')




# =========================== End Filter Option =============================


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
