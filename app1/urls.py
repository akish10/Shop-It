from django.urls import path

from . import views


urlpatterns = [
    path('Home/', views.Home , name = 'Home'),

    path('Login/', views.Login , name = 'Login'),

    path('Signup/', views.Signup , name = 'Signup'),

    path('Insert/', views.Insert , name = 'Insert'),

    path('Delete/', views.Delete , name = 'Delete'),

    path('AllItems/', views.AllItems , name = 'AllItems'),

    path('SellerUpdate/', views.SellerUpdate , name = 'SellerUpdate'),

    path('MakePayment/', views.MakePayment , name = 'MakePayment'),


]