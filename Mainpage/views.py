from django.shortcuts import render,redirect
from django.contrib import messages
from email.message import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import ProductData,CartData,WishlistData,ReviewData,OrderItem
import stripe

def Homepage(request):
    product_data = ProductData.objects.all().values()
    product_datas = ManageProducts(request,product_data)
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("pass")
        cpass = request.POST.get("cpass")
        if password == cpass:
            myuser = User.objects.create_user(email,mobile,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            user = authenticate(username = email,password = password)
            login(request,user)
            messages.success(request,"You are Logged in successfully")
            return redirect("/")
        else:
            messages.warning(request,"Password is not matched ")
            return redirect("/password/")
    return render(request, "Mainpage/index.html",{"product_data":product_datas})

def ManageProducts(request,product_data):
    user = request.user
    wishlistdata = WishlistData.objects.filter(user_id = user.id).values()
    all_products_data = []
    for i in product_data:
        mydic = {}
        mydic["id"] = i["id"]
        mydic["product_name"] = i["product_name"]
        mydic["product_desc"] = i["product_desc"]
        mydic["product_img"] = i["product_img"]
        mydic["product_price"] = i["product_price"]
        mydic["product_cat"] = i["product_cat"]
        mydic["product_qty"] = i["product_qty"]
        mydic["wish_status"] = False
        for j in wishlistdata:
            if i["id"] == j["product_id"]:
                mydic["wish_status"] = True
                break
            else:
                mydic["wish_status"] = False
        all_products_data.append(mydic)
    return all_products_data

def AboutPage(request):
    return render(request,"Mainpage/about.html")

def ProductPage(request):
    product_data = ProductData.objects.all().values()
    product_datas = ManageProducts(request,product_data)
    return render(request,"Mainpage/products.html",{"product_data":product_datas})

def HorizontalPro(request):
    product_data = ProductData.objects.filter(product_cat = "Horizontal").all().values()
    product_datas = ManageProducts(request,product_data)
    return render(request,"Mainpage/products.html",{"product_data":product_datas})

def VerticalPro(request):
    product_data = ProductData.objects.filter(product_cat = "Vertical").all().values()
    product_datas = ManageProducts(request,product_data)
    return render(request,"Mainpage/products.html",{"product_data":product_datas})

def MyProduct(request,id):
    product_data = ProductData.objects.filter(id = id).values().all()
    reviews_data = ReviewData.objects.filter(product_id = id).values().all()
    review_list = []
    for i in reviews_data:
        review_dic = {}
        review_dic["id"] = i['id']
        review_dic["customer_id"] = i["user_id"]
        str = ""
        for j in range(i["review_star"]):
            str = str + "a"
        review_dic["stars"] = str
        review_dic["reviewer_name"] = i["reviewer_name"]
        review_dic["review_text"] = i["review_desc"]
        review_list.append(review_dic)
    return render(request,"Mainpage/myproduct.html",{"product_data":product_data,"reviews_data":review_list})

def SearchPage(request):
    product_data = None
    if request.method == "POST":
        search = request.POST.get("query")
        product_data = ProductData.objects.filter(product_name__icontains = search).values().all()
        product_datas = ManageProducts(request,product_data)
        return render(request,"Mainpage/search.html",{"product_data":product_datas,"search":search})
    return render(request,"Mainpage/search.html",{"product_data":product_data})


def ProfilePage(request):
    return render(request,"Mainpage/profile.html")

def WishlistPage(request):
    user = request.user
    if user.is_authenticated:
        wishlist_data = WishlistData.objects.filter(user_id = user.id).all().values()
        wishlist = WishlistData()
        if request.method == "POST":
            id = request.POST.get("id")
            wishlist.user_id = user.id
            wishlist.product_id = id
            wishlist.save()
            return redirect("/wishlist/")
        mywishlist = []
        for i in wishlist_data:
            mydic = {}
            product_data = ProductData.objects.filter(id = i["product_id"]).values()[0]
            mydic["id"] = i["id"]
            mydic["p_img"] = product_data["product_img"]
            mydic["p_name"] = product_data["product_name"]
            mydic["P_price"] = product_data["product_price"]
            mydic["date"] = i["date"]
            mywishlist.append(mydic)
        return render(request,"Mainpage/wishlist.html",{"wishlist_data":mywishlist})
    else:
        messages.warning(request,"Please Login after then add in wishlist")
        return redirect("/")

def MyordersPage(request):
    user = request.user
    if user.is_authenticated:
        orderitem = OrderItem.objects.filter(user_id = user.id).all().values()
        myorderitem = []
        for i in orderitem:
            mydic = {}
            product_data = ProductData.objects.filter(id = i["product_id"]).values()[0]
            mydic["id"] = i["id"]
            mydic["p_img"] = product_data["product_img"]
            mydic["p_name"] = product_data["product_name"]
            mydic["P_price"] = product_data["product_price"]
            mydic["date"] = i["date"]
            myorderitem.append(mydic)
        return render(request,"Mainpage/orders.html",{"myorderitem":myorderitem})
    return render(request,"Mainpage/orders.html")

def CartPage(request):
    if request.user.is_authenticated == True:
        user = request.user
        cart_data = CartData.objects.filter(user_id = user.id).all().values()
        cart_datas = CartData()
        if request.method == "POST":
            proid = request.POST.get("id")
            qty = int(request.POST.get("qty"))
            amount = int(request.POST.get("amount"))
            cart_datas.product_id = proid
            cart_datas.user_id = user.id
            cart_datas.qty = qty
            cart_datas.amount = amount * qty
            cart_datas.save()
            return redirect("/cart/")
        mycartlist = []
        total_price = 0
        for i in cart_data:
            mydic = {}
            product_data = ProductData.objects.filter(id = i["product_id"]).values()[0]
            mydic["id"] = i["id"]
            mydic["p_img"] = product_data["product_img"]
            mydic["p_name"] = product_data["product_name"]
            mydic["qty"] = i["qty"]
            mydic["P_price"] = i["amount"]
            total_price = total_price + i["amount"]
            mydic["date"] = i["date"]
            mycartlist.append(mydic)
        return render(request,"Mainpage/cart.html",{"cart_data":mycartlist,"total_price":total_price})
    else:
        return redirect("/login/")

def DeleteItem(request):
    if request.method == "POST":
        id = request.POST.get("id")
        CartData.objects.filter(id = id).delete()
        return redirect("/cart/")
    return redirect("/cart/")

def RemoveItem(request):
    if request.method == "POST":
        id = request.POST.get("id")
        WishlistData.objects.filter(id = id).delete()
        return redirect("/wishlist/")
    return redirect("/wishlist/")

def OrderPage(request):
    return render(request,"Mainpage/order.html")

stripe.api_key = 'sk_test_51MedHmSHJDFuPL5cnRItHVU94xOAzKltL5vuoADjGI0wZfVNRtCwU3I3eKgvtQUF0z3w2yl5IuQ5rRZcOs9m2ytj00YSZRJhjw'
def checkout(request):
    user = request.user
    if request.method == "POST":
        total_price = 0
        cart_data = CartData.objects.filter(user_id=user.id).all().values()
        line_items = []
        total_price = 0
        for i in range(0,len(cart_data)):
            product_id = cart_data[i]["product_id"]
            product_data = ProductData.objects.filter(id = product_id).all().values()[0]
            total_price = total_price + product_data["product_price"]
            line_items.append(
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product_data["product_name"],
                    },
                    'unit_amount': int(product_data["product_price"] * 100),
                },
                'quantity': cart_data[i]["qty"],
            })
        session = stripe.checkout.Session.create(
        line_items= line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancle/',
        )
        return redirect(session.url, code=303)
    return redirect('/')

def success_page(request):
    user = request.user
    cart_item = CartData.objects.filter(user_id = user.id).all().values()
    for i in cart_item:
        order_item = OrderItem()
        order_item.product_id = i["product_id"]
        order_item.qty = i["qty"]
        order_item.user_id = user.id
        order_item.save()
    CartData.objects.filter(user_id = user.id).delete()
    return render(request,"Mainpage/success.html")

def cancle_page(request):
    return render(request,"Mainpage/cancle.html")

def EditProfile(request):
    user = request.user
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        User.objects.filter(id = user.id).update(first_name = fname)
        User.objects.filter(id = user.id).update(last_name = lname)
        User.objects.filter(id = user.id).update(username = email)
        return redirect('/profile/')
    return render(request,"Mainpage/edit-profile.html")

def ReviewHandle(request):
    reviews = ReviewData()
    user = request.user
    if request.method == "POST":
        stars = request.POST.get("result")
        product_id = request.POST.get("product_id")
        review = request.POST.get("review")
        username = request.POST.get("username")
        reviews.user_id = user.id
        reviews.product_id = product_id
        reviews.review_desc = review
        reviews.review_star = stars
        reviews.reviewer_name = username
        reviews.save()
        return redirect("/myproduct/{}".format(product_id))
    return redirect("/")

def Logout(request):
    logout(request)
    return redirect("/")