from django.shortcuts import render,redirect

from django.contrib import messages

from django.http import HttpResponse

from django.utils.timezone import now

from datetime import timedelta

from django.shortcuts import get_object_or_404

from .models import *

from .forms import *

#from .mpesa import *

import requests

from django.db.models import Q #enables querying the database.

#from .serializers import *

from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator #for controlling number of items shown in a single page 

#from rest_framework import viewsets


# Create your views here.

#@login_required

"""class InsertView(viewsets.ModelViewSet):

    queryset = Insert.objects.all()

    serializer_class = AddItemSerializer"""

@login_required

def Home(request):#logic done 

    return render(request,'home.html')

def landingPage(request): #handling landing page

    return render(request,'landing.html')

def Login(request): #done 

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']

            password = form.cleaned_data['password']

            user = authenticate(request, username = username , password = password)

            if user is not None :

                login(request,user)

                return redirect('Home')

            else:

                return render(request,'login.html',{'form':form,'error':'Invalid credentials.'})

    else:

        form = LoginForm()



    return render(request,'login.html',{'form':form})


def Signup(request): #done 

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('Home')
    
    else:

        form = UserForm()


    return render(request,'register.html', {'form':form })



@login_required

def Insert(request): #done 

    message = None

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == "add":

            form = AddItemForm(request.POST, request.FILES)

            if form.is_valid():

                add_item = form.save(commit=False)

                add_item.username = request.user

                add_item.save()

                message = 'Item added successfully.'

        elif action == 'remove':

            item_name = request.POST.get('item_name')

            item = AddItem.objects.filter(seller=request.user, item_name=item_name).first()

            if item:

                time_difference = timezone.now() - item.date_added

                if time_difference <= timedelta(days=1):

                    item.delete()

                    message = 'Item removed successfully.'

                else:

                    message = "Cannot remove item after 24 hours."

            else:

                message = 'Item not found.'

   
    form = AddItemForm()


    return render(request, 'addItem.html', {'form': form, 'message': message})


@login_required

def SellerUpdate(request): #done 

    item = request.GET.get('item_name')

    item_get = get_object_or_404(AddItem, item_name = item, seller= request.user)

    if request.method == 'POST':

        form = UpdateItemDetails(request.POST,request.FILES , instance=item_get)

        if form.is_valid():

            update = form.save()

            messages.success(request,'Item details updated successfully.')


            #return render(request,'seller_update.html',{'form':form})

        else:

            messages.error(request,'Item updates not applied.')


    else:

        form = AddItemForm(instance = item_get)

        
    return render(request,'seller_update.html',{'form':form, 'item':item_get})


@login_required

def AllItems(request): #done 

    
    items = AddItem.objects.all() 
    
    paginator = Paginator(items, 10)  

    page_number = request.GET.get('page')  

    page_obj = paginator.get_page(page_number)
    
    return render(request, 'allItems.html', {'items': items,'page_obj':page_obj})



@login_required

def orders(request):

    item_id = request.GET.get('item_id')

    item = get_object_or_404(AddItem, id=item_id) if item_id else None

    user = request.user

    form = OrderForm(initial={'item':item})

    if request.method == 'POST':

        form = OrderForm(request.POST)

        if form.is_valid():

            order_quantity = form.cleaned_data['quantity']
            
            if order_quantity > item.quantity:

                messages.error(request, f"Not enough stock available. Only {item.quantity} left.")
            else:
                
                order = form.save(commit=False)

                order.user = user

                order.item = item

                order.save()

                item.quantity -= order_quantity

                item.save()

                CartItem.objects.create(user=user,item=item,quantity = order_quantity)

                messages.success(request, "Order placed successfully!")

                return redirect('AllItems') 

        form = OrderForm(initial={'item': item})

    return render(request, 'orders.html', {'form': form, 'item': item})




@login_required

def added_to_cart(request): #items added to cart

    cart_items = CartItem.objects.filter(user=request.user)

    orders = Order.objects.filter(user=request.user)

    cart_total = sum(item.subtotal for item in cart_items)
    
    order_total = sum(order.item.price * order.quantity for order in orders)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': cart_total,
        'orders': orders, 
        'order_total': order_total, 
    })


def remove_from_cart(request,item_id):

    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    item = cart_item.item

    quantity_to_remove = cart_item.quantity

    cart_item.delete()

    Order.objects.filter(user=request.user, item=item).filter(quantity=quantity_to_remove).delete()

    
    item.quantity += quantity_to_remove

    item.save()

    Order.objects.filter(user=request.user, item=item).filter(quantity=quantity_to_remove).delete()

    messages.success(request, f"{item.item_name} has been removed from your cart.")
    

    return redirect('added_to_cart')

def checkout(request):

    return render(request,'pay.html')
    
    
    

"""@login_required

def add_to_cart(request):

    if request.method == 'POST':

        item_id = request.POST.get('item_id')

        item = AddItem.objects.get(id=item_id)

        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, item=item
        )
        
        if not created:
            
            cart_item.quantity += 1

            cart_item.save()

        return redirect('added_to_cart')

"""


def checkout(request):

    return render(request,'cart.html')


def Logout(request):

    logout(request)

    return redirect('Login')

#def mpesa(request):

    #return render(request,'mpesa.html')


#@login_required

"""def Cart(request,item_id): #for storing items that user has selected.

    #item = request.GET.get('item_name')

    item = AddItem.objects.get(id=item_id)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    return redirect('ViewCart')

    '''item = AddItem.objects.get(id = item_id)

    cart = request.session.get('cart',[])

    for cart_item in cart:

        if cart_item['item_id'] == item.id:

            cart_item['quantity'] += 1

            request.session['cart'] = cart

            return redirect('ViewCart')

    cart_item = {
        'item_id':item.id,

        'item_name': item.item_name,

        'price':float(item.price),

        'quantity': 1, #return render(request,'cart.html')

    }

    cart.append(cart_item)

    request.session['cart'] = cart

    return redirect('ViewCart')'''

def RemoveFromCart(request, item_id):

    cart = request.session.get('cart', [])

    cart = [item for item in cart if item['item_id'] != item_id]  # Remove the specific item

    request.session['cart'] = cart  # Save updated cart back to the session

    return redirect('ViewCart')


#@login_required

def ViewCart(request):
    #shows all items in the cart from Cart view.

    #cart = request.session.get('cart', [])

    #total = sum(item['price'] * item['quantity'] for item in cart)

    cart_items = CartItem.objects.filter(user=request.user)

    total = sum([item.subtotal() for item in cart_items]) 

    return render(request,'cart.html',{'cart':cart,'total':total})

def checkout(request): #confirm payment before deleting item from database

    cart_items = CartItem.objects.filter(user=request.user)

    total = sum([item.subtotal() for item in cart_items])

    if request.method == 'POST':
        for cart_item in cart_items:
            # Create a transaction for each cart item
            Transaction.objects.create(
                cart_item=cart_item,
                quantity_paid=cart_item.quantity,
                buyer=request.user
            )
            # After payment, you can choose to delete the cart items
            cart_item.delete()

        return redirect('payment_success')
        
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

#@login_required

def MakePayment(request):

    cart  = request.session.get('cart',[])

    if not cart:

        messages.error(request,'No items in cart')

        return redirect('AllItems')

    if cart and request.method == 'POST':

        for item in cart:

            BoughtItem.objects.create(

                buyer = request.user,

                item_bought_id = item['item_id'],

                quantity_bought = item['quantity'],

                price_bought = item['price'],

                date_bought = now(),
            )

        
        request.session['cart'] = []

        messages.success(request,'Payment successful, Thanks for shopping with us.')

    return render(request,'make_payment.html')


def pay(request):

    if request.method == "POST":

        
        form = PayForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('Home')
    
    else:

        form = PayForm()

    return render(request,'pay.html',{'form':form})


def stkPush(request):

    if request.method == 'POST':

        phone = request.POST.get('phone_number')

        name = request.POST.get('name')

        amount = request.POST.get('amount')

        access_token =AccessToken.access_token

        apiUrl = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        header = {'Authorization':'Bearer %s'% access_token}

        request = {    
   "BusinessShortCode":Password.shortcode,
   "Password":Password.decoded_password,
   "Timestamp":Password.timestamp,   
   "TransactionType": "CustomerPayBillOnline",    
   "Amount": amount,    
   "PartyA":pnone,    
   "PartyB":Password.shortcode,    
   "PhoneNumber":phone,    
   "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa",    
   "AccountReference":"Winnie",    
   "TransactionDesc":"Makepayment."
}

    
    response = requests.post(apiUrl,json=request,header=header)
    return HttpResponse('success')

def MakePayment(request):

    if request.method == 'POST':

        form = TransactionsForm(request.POST)

        message = None

        if form.is_valid():

            transact = form.save()

            message = 'Transaction successful'

            messages.success(request,message)

        else:

            message = 'Transaction failed'

    
            messages.error(request,message)

    else:
    
        form = TransactionsForm()
            

    return render(request,'make_payment.html',{'form':form})
  
#def Search(request): for implementing search functionality.

    #query = 

@login_required

def Delete(request):

    return render(request,'allItems.html')


@login_required

def ViewTransaction(request):

    return render(request,'transactions.html')"""


