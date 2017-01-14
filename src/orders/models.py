from django.conf import settings
from django.db import models
from carts.models import Cart
from decimal import Decimal

from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save

# Create your models here.

class UserCheckout(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,null=True,blank=True)
	email=models.EmailField(unique=True)
	otp_id=models.CharField(max_length=120,null=True,blank=True)



	def __str__(self):
		return self.email
ADDRESS_TYPE= (
	('billing','Billing'),
	('shipping','Shipping'),
	)

class UserAddress(models.Model):
	user=models.ForeignKey(UserCheckout)
	type=models.CharField(max_length=120,choices=ADDRESS_TYPE)
	mobileNumber=models.CharField(max_length=120,null=True,blank=True)
	street=models.CharField(max_length=120)
	city=models.CharField(max_length=120)
	state=models.CharField(max_length=120)
	zipcode=models.CharField(max_length=120)

	def __str__(self):
		return self.street

	def get_address(self):
		return ("%s,%s,%s-%s" %(self.street,self.city,self.state,self.zipcode))

	def get_mobile_number(self):
		return("%s"%(self.mobileNumber))


ORDER_STATUS_CHOICES=(('created','Created'),
	('completed','Completed'),
	('shipped','Shipped'),
	('delivered','Delivered'))

class Order(models.Model):
	status=models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='Created')
	cart=models.ForeignKey(Cart)
	user=models.ForeignKey(UserCheckout,null=True)
	billing_address=models.ForeignKey(UserAddress,related_name="billing_address",null=True)
	shipping_address=models.ForeignKey(UserAddress,related_name="shipping_address",null=True)
	# mobile_number=models.ForeignKey(UserAddress,related_name="mobile_number",null=True)
	shipping_total_price=models.DecimalField(decimal_places=2,max_digits=50,default=50)
	order_total=models.DecimalField(decimal_places=2,max_digits=50)

	def __str__(self):
		return str(self.cart.id)

	class Meta:
		ordering=['-id']

	def mark_completed(self):
		self.status="completed"
		self.save()
	
	def mark_shipped(self):
		self.status="shipped"
		self.save()
	
	def mark_delivered(self):
		self.status="delivered"
		self.save()

	def get_absolute_url(self):
		return reverse("order_detail",kwargs={'pk':self.pk})
  
def order_pre_save(sender,instance,*args,**kwargs):
	shipping_total_price=instance.shipping_total_price
	cart_total=instance.cart.total
	order_total=Decimal(shipping_total_price)+ Decimal(cart_total)
	instance.order_total=order_total

  
pre_save.connect(order_pre_save,sender=Order)