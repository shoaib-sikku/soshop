from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer , Product , OrderPlaced , Cart
from .forms import Registraion,CustomerForm
from django.contrib import messages
from .forms import LoginForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# client.set_app_details({"title" : "Django", "version" : "4.1.3"})

class ProductView(View):
    def get(self,request):
        topwear= Product.objects.filter(category='TW')
        bottomwear= Product.objects.filter(category='BW')
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        cart_items = ''
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)
        return render(request,'app/home.html',{'topwear':topwear,'bottomwear':bottomwear,'mobile':mobile,"laptop":laptop,'cart_items':len(cart_items)})

# /product-detail------
class ProductDetailView(View):
    def get(self,request,slug):
        product = Product.objects.get(slug=slug)
        already_in_cart = False
        if request.user.is_authenticated:
            already_in_cart = Cart.objects.filter(Q(user=request.user)&Q(product=product)).exists()
        return render(request,'app/productdetail.html',{'product':product,'already_in_cart':already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('addtocart')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart/')

@login_required
def buynow(request):
    user = request.user
    product_id = request.GET.get('buynow')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/checkout/')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        amt=0.0
        shipping_amt=50.0
        total_amt=0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for p in cart_product:
                tempamt=(p.quantity*p.product.selling_price)
                amt += tempamt
                total_amt = amt+shipping_amt 
        return render(request,'app/addtocart.html',{"carts":carts,"amt":amt,"total_amt":total_amt})
        # else:
        #     return render(request,'app/emty.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user) & Q(product=prod_id))
        c.quantity += 1
        c.save()
        amt=0.0
        shipping_amt=50.0
        total_amt=0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for p in cart_product:
                tempamt=(p.quantity*p.product.selling_price)
                amt += tempamt
                total_amt = amt+shipping_amt
            data={
                'quantity':c.quantity,
                'amt':amt,
                'total_amt':total_amt
            }
            return JsonResponse(data) 

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user) & Q(product=prod_id))
        c.quantity -= 1
        c.save()
        amt=0.0
        shipping_amt=50.0
        total_amt=0.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for p in cart_product:
                tempamt=(p.quantity*p.product.selling_price)
                amt += tempamt
            data={
                'quantity':c.quantity,
                'amt':amt,
                'total_amt':total_amt+shipping_amt
            }
            return JsonResponse(data) 

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(user=request.user) & Q(product=prod_id))
        c.delete()
        amt=0.0
        shipping_amt=50.0
        cart_product = [p for p in Cart.objects.filter(user=request.user)]
        if cart_product:
            for p in cart_product:
                tempamt=(p.quantity*p.product.selling_price)
                amt += tempamt
            data={
                'amt':amt,
                'total_amt':amt+shipping_amt
            }
            return JsonResponse(data) 


# profile-----------
class Profile(View):
    def get(self,request):
        if request.user.is_authenticated:
            fm = CustomerForm()
            return render(request,'app/profile.html',{'form':fm,'active':'btn-primary'})
        else:
            return redirect('/accounts/login/')
        
    def post(self,request):
        fm = CustomerForm(request.POST)
        if fm.is_valid():
            usr = request.user
            name = fm.cleaned_data['name']
            locality = fm.cleaned_data['locality']
            city = fm.cleaned_data['city']
            state = fm.cleaned_data['state']
            zipcode = fm.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            fm = CustomerForm()
        return render(request,'app/profile.html',{'form':fm,'active':'btn-primary'})

# /address--------------
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})
# /orders------
@login_required
def orders(request):
    order = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{"order":order})


# /mobile-----------
def mobile(request,data=None):
    if data==None:
        mobiles = Product.objects.filter(category='M')
    elif data=='realme' or data=='apple':
        mobiles =Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles =Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mobiles =Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobile':mobiles})

# /laptop-------------
def laptop(request,data=None):
    if data==None:
        laptops = Product.objects.filter(category='L')
    elif data=='dell' or data=='hp':
        laptops =Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptops =Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data=='above':
        laptops =Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    return render(request, 'app/laptop.html',{'laptops':laptops})

# /topwear-------------
def topwear(request,data=None):
    if data==None:
        topwears = Product.objects.filter(category='TW')
    # elif data=='dell' or data=='hp':
    #     topwears =Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        topwears =Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data=='above':
        topwears =Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/topwear.html',{'topwears':topwears})

# /bottomwear-------------
def bottomwear(request,data=None):
    if data==None:
        bottomwears = Product.objects.filter(category='BW')
    elif data=='below':
        bottomwears =Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data=='above':
        bottomwears =Product.objects.filter(category='BW').filter(discounted_price__gt=500)
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})

# registration-------------
class RegistraionView(View):
    def get(self,request):
        form = Registraion()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        if request.method=='POST':
            form = Registraion(request.POST)
            if form.is_valid():
                messages.success(request,'Congulatutions, You are registered!!')
                form.save()
                form = Registraion()
        return render(request,'app/customerregistration.html',{'form':form})
        
# /checkout-------------
@csrf_exempt
def checkout(request):
    c = Cart.objects.filter(user=request.user)
    add = Customer.objects.filter(user=request.user)
    amt=0.0
    shipping_amt=50.0
    cart_product = [p for p in Cart.objects.filter(user=request.user)]
    if cart_product:
        for p in cart_product:
            tempamt=(p.quantity*p.product.selling_price)
            amt += tempamt
            grandtotal = amt+shipping_amt 
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
    data = { "amount": grandtotal*100, "currency": "INR",}
    payment = client.order.create(data=data)
    payment_order_id = payment['id']
    return render(request, 'app/checkout.html',{'add':add,"c":c,"grandtotal":grandtotal,'api_key':settings.RAZORPAY_KEY_ID,'order_id':payment_order_id,'amt':grandtotal*100})
 
# /paymentdone-------------

def paymentdone(request):
    if request.method == 'GET': 
        id = request.GET['addid']
        customer = Customer.objects.get(id=id)
        cart = Cart.objects.filter(user=request.user)
        for i in cart:
            var = OrderPlaced(user=request.user,customer=customer,product=i.product,quantity=i.quantity,)
            var.save()
            i.delete()
        return redirect('/orders/')