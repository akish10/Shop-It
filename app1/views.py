from django.shortcuts import render,redirect

from django.contrib import messages

from django.utils.timezone import now

from datetime import timedelta

from django.shortcuts import get_object_or_404

from .models import *

from .forms import *

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

def Home(request):#done 

    return render(request,'home.html')


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


def mpesa(request):

    return render(request,'mpesa.html')


@login_required

def Cart(request,item_id): #for storing items that user has selected.

    #item = request.GET.get('item_name')

    item = AddItem.objects.get(id = item_id)

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

    return redirect('ViewCart')

@login_required

def ViewCart(request):
    #shows all items in the cart from Cart view.

    cart = request.session.get('cart', [])

    total = sum(item['price'] * item['quantity'] for item in cart)


    return render(request,'cart.html',{'cart':cart,'total':total})

@login_required

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


"""def MakePayment(request):

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
            

    return render(request,'make_payment.html',{'form':form})"""
  
#def Search(request): for implementing search functionality.

    #query = 

@login_required

def Delete(request):

    return render(request,'allItems.html')


@login_required

def ViewTransaction(request):

    return render(request,'transactions.html')


def Logout(request):

    logout(request)

    return redirect('Login')