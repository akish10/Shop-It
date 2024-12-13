from django.urls import path

from . import views


urlpatterns = [
    path('Home/', views.Home , name = 'Home'), #for dashboard

    path('Login/', views.Login , name = 'Login'), # login page 

    path('Signup/', views.Signup , name = 'Signup'), # signup

    path('Insert/', views.Insert , name = 'Insert'), # insert

    path('', views.landingPage , name = 'landingPage'), #homepage

    path('AllItems/', views.AllItems , name = 'AllItems'), #all items

    path('Logout/', views.Logout , name = 'Logout'), #logout 

    path('orders/', views.orders , name = 'orders'),

    path('added_to_cart/', views.added_to_cart, name = 'added_to_cart'),

    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('MakePayment/', views.MakePayment , name = 'Payment'),


    #path('add_to_cart/', views.add_to_cart , name = 'add_to_cart'),

    #path('Delete/', views.Delete , name = 'Delete'),

    #path('SellerUpdate/', views.SellerUpdate , name = 'SellerUpdate'),

    #path('MakePayment/', views.MakePayment , name = 'MakePayment'),

    #path('Cart/<int:item_id>/', views.Cart, name = 'Cart'),

    #path('RemoveFromCart/<int:item_id>/', views.RemoveFromCart, name='RemoveFromCart'),

    #path('ViewCart/', views.ViewCart , name = 'ViewCart'),

    #path('pay/', views.pay , name = 'pay'),

    #path('stkPush', views.stkPush , name = 'stkPush'),


]