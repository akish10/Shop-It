from django.db import models

from django.conf import settings


# Create your models here.



class AddItem(models.Model): #items added on website

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items_sold')

    item_name = models.CharField(max_length=50)

    quantity = models.IntegerField()

    price = models.DecimalField(max_digits=9, decimal_places=2)

    location = models.CharField(max_length=50)

    image = models.ImageField()

    description = models.TextField(max_length=300)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.item_name




class BoughtItem(models.Model): #bought items

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items_bought')

    item_bought = models.ForeignKey(AddItem, on_delete=models.CASCADE, related_name='purchases')

    quantity_bought = models.IntegerField()

    price_bought = models.DecimalField(max_digits=9, decimal_places=2)

    date_bought = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.item.item_name} bought by {self.buyer.username}"


class UpdateItemDetails(models.Model): #updated by owner of goods

    seller_update = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updates_made')

    item_update = models.ForeignKey(AddItem,on_delete=models.CASCADE,related_name='update_requests')

    quantity_update = models.IntegerField()

    reset_price = models.DecimalField(max_digits=9, decimal_places=2)

    reset_description = models.TextField(max_length=300)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):


        return f"Update request for {self.item.item_name} by {self.seller.username}"


class Transactions(models.Model):

     item_paid = models.ForeignKey(BoughtItem,on_delete=models.CASCADE,related_name='transaction_requests')

     quantity_paid = models.IntegerField()

     buyer_paid = models.ForeignKey(BoughtItem,on_delete=models.CASCADE,related_name='buyer_transactions')

     def __str__(self):

        return f"Transaction for {self.item_paid} by {self.buyer_paid}" 


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_items')

    item = models.ForeignKey(AddItem, on_delete=models.CASCADE, related_name='order_items')

    quantity = models.PositiveIntegerField(default=1)

    time  = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"Order by {self.user.username} for {self.item.item_name}"




class CartItem(models.Model): # store cart items

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')

    item = models.ForeignKey(AddItem, on_delete=models.CASCADE, related_name='cart_items')

    quantity = models.PositiveIntegerField(default=1)

    @property
    
    def subtotal(self):

        return self.quantity * self.item.price

    def __str__(self):

        return f"{self.quantity} x {self.item.item_name} for {self.user.username}"



class Pay(models.Model): #handling mpesa stk form

    phone_number = models.IntegerField()

    name = models.CharField(max_length=50)

    amount = models.DecimalField(max_digits=7, decimal_places=2)

    transaction_status = models.BooleanField()

    time_paid = models.DateTimeField(auto_now=True)

   