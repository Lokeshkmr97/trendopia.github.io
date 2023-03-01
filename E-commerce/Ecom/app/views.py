from django.shortcuts import render,redirect
from django.views import View
from .models import Cart,Customer,Product,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm,ContactForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]

        if cart_product:
            for p in cart_product:
                temp_amount=(p.quantity*p.product.discounted_price)   # p.product ka matlab hai p se cart wala value melege 
                                                                        #aur product se product table wala value milega
                amount+=temp_amount
                if amount>700:
                    shipping_amount=0.0
                total_amount=amount+shipping_amount
        if amount==0.0:
            shipping_amount=0.0
        return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount,'Shipping_amount':shipping_amount})
    
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount=(p.quantity*p.product.discounted_price)   # p.product ka matlab hai p se cart wala value melege 
                                                                    #aur product se product table wala value milega
            amount+=temp_amount
            if amount>700:
                shipping_amount=0.0
            total_amount=amount+shipping_amount        

        if amount==0.0:
            shipping_amount=0.0
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount,
            'shipping_amount':shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity>1:
            c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount=(p.quantity*p.product.discounted_price)   # p.product ka matlab hai p se cart wala value melege 
                                                                    #aur product se product table wala value milega
            amount+=temp_amount
            if amount>700:
                shipping_amount=0.0
            total_amount=amount+shipping_amount        

        if amount==0.0:
            shipping_amount=0.0
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount,
            'shipping_amount':shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount=(p.quantity*p.product.discounted_price)   # p.product ka matlab hai p se cart wala value melege 
                                                                    #aur product se product table wala value milega
            amount+=temp_amount
            if amount>700:
                shipping_amount=0.0
            total_amount=amount+shipping_amount        

        if amount==0.0:
            shipping_amount=0.0
        data={
            'amount':amount,
            'totalamount':total_amount,
            'shipping_amount':shipping_amount
        }
        return JsonResponse(data)
   




@login_required
def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})


def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Redmi' or data=='OnePlus' or data=='Oppo' or data=='Realme' or data=='iphone':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def bottom_wear(request,data=None):
    if data==None:
        bottomwear=Product.objects.filter(category='BW')
    elif data=='Leecopper' or data=='Puma' or data=='Nike' or data=='Levis' or data=='Killer':
        bottomwear=Product.objects.filter(category='BW').filter(brand=data)
    # elif data=='below':
    #     bottomwear=Product.objects.filter(category='BW').filter(discounted_price__lt=10000)
    # elif data=='above':
    #     bottomwear=Product.objects.filter(category='BW').filter(discounted_price__gt=10000)
    return render(request, 'app/bottomwear.html',{'bottomwear':bottomwear})

def top_wear(request,data=None):
    if data==None:
        topwear=Product.objects.filter(category='TW')
    elif data=='Leecopper' or data=='LouisVuitton' or data=='Nike' or data=='Zara' or data=='Gucci' or data=='Adidas':
        topwear=Product.objects.filter(category='TW').filter(brand=data)
    # elif data=='below':
    #     topwear=Product.objects.filter(category='TW').filter(discounted_price__lt=10000)
    # elif data=='above':
    #     topwear=Product.objects.filter(category='TW').filter(discounted_price__gt=10000)
    return render(request, 'app/topwear.html',{'topwear':topwear})


def laptop(request,data=None):
    if data==None:
        laptop=Product.objects.filter(category='L')
    elif data=='Lenovo' or data=='Acer' or data=='Hp' or data=='Apple' or data=='Asus':
        laptop=Product.objects.filter(category='L').filter(brand=data)
    # elif data=='below':
    #     topwear=Product.objects.filter(category='L').filter(discounted_price__lt=10000)
    # elif data=='above':
    #     topwear=Product.objects.filter(category='L').filter(discounted_price__gt=10000)
    return render(request, 'app/laptop.html',{'laptop':laptop})


class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            # messages.SUCCESS(request,'Congratulation ! User Registered Successfully')
            messages.add_message(request, messages.INFO, 'Congratulation ! User Registered Successfully')
            form.save()
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})


@login_required
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 total_amount=0.0
 cart_product=[p for p in Cart.objects.all() if p.user==user]
 if cart_product:
    for p in cart_product:
        temp_amount=(p.quantity*p.product.discounted_price)   
        amount+=temp_amount
        if amount>700:
            shipping_amount=0.0
        total_amount=amount+shipping_amount        

    if amount==0.0:
        shipping_amount=0.0

 return render(request, 'app/checkout.html',{'add':add,'totalamount':total_amount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user # current user show with help of request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.add_message(request, messages.INFO, 'Record Save Successfully !')
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})


def privacypolicy(request):
    return render(request,'app/privacypolicy.html')      

def return_refund_policy(request):
    return render(request,'app/return_refund_policy.html') 

def contact(request):
    if request.method=="POST":
        fm=ContactForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.add_message(request, messages.INFO, 'Thanks for contact with us')
            fm=ContactForm()
    else:
        fm=ContactForm()       

    return render(request,'app/contact.html',{'form':fm})

def shipping_policy(request):
    return render(request,'app/shipping_policy.html')

def term_condition(request):
    return render(request,'app/term_condition.html')


    


# https://source.unsplash.com/ecommerce

    
    