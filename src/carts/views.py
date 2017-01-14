from django.contrib import messages
from django.http import HttpResponseRedirect,Http404, JsonResponse
from django.shortcuts import render,get_object_or_404,redirect

from django.core.urlresolvers import reverse

from django.contrib.auth.forms import AuthenticationForm

from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin,DetailView
from django.views.generic.edit import FormMixin

from products.models import variation
from carts.models import Cart,CartItem

from orders.forms import GuestCheckoutForm
from orders.models import UserCheckout,Order,UserAddress

from orders.mixins import CartOrderMixin

import random
from django.conf import settings
from twilio.rest import TwilioRestClient

from django.conf import settings
from django.core.mail import send_mail

from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

# Create your views here.


class ItemCountView(View):


	def get(self,request,*args,**kwargs):

		if request.is_ajax:
			cart_id=self.request.session.get("cart_id")
			if cart_id==None:
				count= 0
			else:
				cart=Cart.objects.get(id=cart_id)
				count=cart.items.count()
			request.session["cart_item_count"]=count

			return JsonResponse({"count":count})
		else:
			raise Http404




class cartview(SingleObjectMixin,View):
	model = Cart
	template_name="carts/view.html"
	def get_object(self,*args,**kwargs):
		self.request.session.set_expiry(0)
		cart_id=self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id

		cart=Cart.objects.get(id=cart_id)

		if self.request.user.is_authenticated():
			cart.user=self.request.user
			cart.save()
		return cart 

	def get(self,request,*args,**kwargs):
		cart=self.get_object()
		

		item_id=request.GET.get("item")
		delete_item=request.GET.get("delete",False)
		if item_id:
			item_instance=get_object_or_404(variation,id=item_id)
			qty=request.GET.get("qty",1)
			flash_message=""
			item_added=False
			try:
				if int(qty)<1:
					delete_item=True
			except:
				raise Http404
			
			cart_item,created=CartItem.objects.get_or_create(cart=cart,item=item_instance)
			
			if created:
				item_added=True
				flash_message="Product sucessfully added !!"
			if delete_item:
				flash_message="Item removed sucessfully"
				cart_item.delete()
			else:
				if not created:
					flash_message="quantity has been updated sucessfully"
				cart_item.quantity=qty
				cart_item.save()
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("carts"))
		if request.is_ajax():
			try:
				total=cart_item.line_item_total
			except:
				total=None
			try:
				subtotal=cart_item.cart.subtotal
			except:
				subtotal=None
			try:
				total_items=cart_item.cart.items.count()
			except:
				total_items=0

			try:
				taxtotal=cart_item.cart.taxtotal
			except:
				taxtotal=None
			try:
				total=cart_item.cart.total
			except:
				total=None


			data={
				"deleted":delete_item,
				"item_added":item_added,
				"line_total": total,
				"subtotal":subtotal,
				"flash_message":flash_message,
				"total_items":total_items,
				"taxtotal":taxtotal,
				"total":total
				}

			return JsonResponse(data)	

		context={
				"object": self.get_object()

		}
		template=self.template_name
		return render(request,template,context)



class CheckoutView(CartOrderMixin,FormMixin,DetailView):
	model=Cart
	template_name="carts/checkout_view.html"
	form_class=GuestCheckoutForm


	def get_object(self,*args,**kwargs):
		cart=self.get_cart()
		if cart == None:
			return None
		return cart 

	def get_context_data(self,*args,**kwargs):
		context=super(CheckoutView,self).get_context_data(*args,**kwargs)

		#cart=self.get_object()
 
		user_can_continue=False
		user_check_id=self.request.session.get('user_checkout_id')
		
		# if not self.request.user.is_authenticated() or user_check_id==None:
		# 	context['login_form']=AuthenticationForm()
		# 	context['next_url']=self.request.build_absolute_uri()
		# elif self.request.user.is_authenticated() or user_check_id!=None:
		# 	user_can_continue=True
		# else:
		# 	pass
		if self.request.user.is_authenticated():
			user_can_continue=True
			user_checkout,created=UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user=self.request.user
			user_checkout.save()
			self.request.session['user_checkout_id']=user_checkout.id

		elif not self.request.user.is_authenticated() and user_check_id==None:
			context['login_form']=AuthenticationForm()
			context['next_url']=self.request.build_absolute_uri()
		else:
			pass

		if user_check_id!=None:
			user_can_continue=True


		context['order']=self.get_order()
		context['user_can_continue']=user_can_continue
		context['form']=self.get_form()	
		return context

	def post(self,request,*args,**kwargs):
		self.object=self.get_object()
		form=self.get_form()
		if form.is_valid():
			email = (form.cleaned_data.get('email'))
			user_checkout,created=UserCheckout.objects.get_or_create(email=email)
			request.session['user_checkout_id']=user_checkout.id
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse('checkout')

	def get(self,request,*args,**kwargs):
		get_data=super(CheckoutView,self).get(request,*args,**kwargs)
		cart=self.get_object() 
		if cart==None:
			return redirect("carts")
		new_order=self.get_order()
		user_checkout_id=request.session.get("user_checkout_id")
		if user_checkout_id !=None:
			user_checkout =UserCheckout.objects.get(id=user_checkout_id)
			if new_order.billing_address==None or new_order.shipping_address==None:
			 	return redirect("order_address")
		
			
			new_order.user=user_checkout
			new_order.save()


		return get_data


 


class CheckoutFinalView(CartOrderMixin,View):
	def post(self,request,*args,**kwargs):
		order=self.get_order()
		if (request.POST.get("payment_token"))=="ABC":
			order.mark_completed()
			print("your mail id is %s"%(order.user.email))
			to_email=order.user.email
			from_email=settings.EMAIL_HOST_USER
			subject=("Order has be completed")
			message=(""" 
				 Hello,
				 The order you have placed has been completed and 
				 will be delivered with in 3-4 working days
				 to get order detail
				 click this link http://127.0.0.1:8000/orders/%s/
				 or http://www.ShimogaWatches.in/orders/%s/
				 Regards,
				 Team ShimogaWatches.in
			 """%(order.pk,order.pk))

			send_mail(subject,message,from_email,[to_email],fail_silently=False,)
			

			messages.success(request,"Thank you for your order")
			del request.session["cart_id"]
			del request.session["order_id"]
			
		return redirect("order_detail",pk=order.pk)

	def get(self,request,*args,**kwargs):
		return redirect("checkout")



def _get_pin(length=5):
    """ Return a numeric PIN with length digits """
    return random.sample(range(10**(length-1), 10**length), 1)[0]


def _verify_pin(mobile_number, pin):
    """ Verify a PIN is correct """
    return pin == cache.get(mobile_number)


def ajax_send_pin(request):
    """ Sends SMS PIN to the specified number """
    mobile_number = request.POST.get('mobile_number', "")
    print(mobile_number)
    if not mobile_number:
        return HttpResponse("No mobile number", mimetype='text/plain', status=403)

    pin = _get_pin()

    # store the PIN in the cache for later verification.
    cache.set(mobile_number, pin, 24*3600) # valid for 24 hrs

    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
                        body="%s" % pin,
                        to=mobile_number,
                        from_=settings.TWILIO_FROM_NUMBER,
                    )
    return HttpResponse("Message %s sent" % message.sid, mimetype='text/plain', status=200)

def process_order(request):
    """ Process orders made via web form and verified by SMS PIN. """
    form = OrderForm(request.POST or None)

    if form.is_valid():
        pin = int(request.POST.get("pin", "0"))
        mobile_number = request.POST.get("mobile_number", "")

        if _verify_pin(mobile_number, pin):
            form.save()
            return redirect("order_detail",pk=order.pk)
        else:
            messages.error(request, "Invalid PIN!")
    else:
        return render(
                    request,
                    'order.html',
                    {
                        'form': form
                    }
                )


