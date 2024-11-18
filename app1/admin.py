from django.contrib import admin

# Register your models here.

from .models import  * #AddItem,BoughtItem,UpdateItemDetails,Transactions


admin.site.register(AddItem)

admin.site.register(BoughtItem)

admin.site.register(UpdateItemDetails)

admin.site.register(Transactions)

