from decimal import Decimal

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save,post_save,post_delete
from django.db import models

from products.models import variation

# Create your models here

class CartItem(models.Model):
	cart=models.ForeignKey('Cart')
	item=models.ForeignKey(variation)
	quantity=models.PositiveIntegerField(default=1)
	line_item_total=models.DecimalField(max_digits=10,decimal_places=2)

	def __str__(self):
		return self.item.title

	def remove(self):
		return self.item.remove_from_cart()

	def get_title(self):
		return "%s - %s" %(self.item.products.title,self.item.title)	

def cart_item_pre_save_reciver(sender,instance,*args,**kwargs):
	qty=instance.quantity
	if int(qty)>=1:
		price=instance.item.get_price()
		line_item_total=Decimal(qty)*Decimal(price)
		instance.line_item_total=line_item_total

pre_save.connect(cart_item_pre_save_reciver,sender=CartItem)


def cart_item_post_save_receiver(sender,instance,*args,**kwargs):
	instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem )

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
	items = models.ManyToManyField(variation,through=CartItem)
	timestamp=models.DateTimeField(auto_now_add=True, auto_now=False)
	updated=models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal=models.DecimalField(max_digits=50,decimal_places=2,default=0.00)
	taxtotal=models.DecimalField(max_digits=50,decimal_places=2,default=0.00)
	total=models.DecimalField(max_digits=50,decimal_places=2,default=0.00)
	taxpercent=models.DecimalField(max_digits=50,decimal_places=5,default=0.00)


	def __str__(self):
		return str(self.id)


	def update_subtotal(self):
		subtotal=0
		items = self.cartitem_set.all()
		for item in items:
			subtotal += item.line_item_total
		self.subtotal ="%.2f" %(subtotal)
		self.save()


	#item
	#timestamp
	#updated
	#subtotal
def do_tax_and_total_receiver(sender,instance,*args,**kwargs):
	subtotal=Decimal(instance.subtotal)
	taxtotal=round(subtotal*Decimal(instance.taxpercent),2) #8.5
	total=round(subtotal+taxtotal,2)
	instance.taxtotal="%.2f"%(taxtotal)
	instance.total="%.2f"%(total)

pre_save.connect(do_tax_and_total_receiver,sender=Cart)
