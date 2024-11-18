from django.shortcuts import render,redirect

from django.contrib import messages

from django.utils.timezone import now

from datetime import timedelta

from django.shortcuts import get_object_or_404

from .models import *

from .forms import *

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

def Home(request):

    return render(request,'home.html')


def Login(request): #done 

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            username = authenticate(request, username = username , password = password)

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
    
    paginator = Paginator(items, 9)  

    page_number = request.GET.get('page')  

    page_obj = paginator.get_page(page_number)
    
    return render(request, 'allItems.html', {'items': items,'page_obj':page_obj})




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
  


def Delete(request):

    return render(request,'allItems.html')



def ViewTransaction(request):

    return render(request,'transactions.html')


def Logout(request):

    logout(request)

    return redirect('Login')