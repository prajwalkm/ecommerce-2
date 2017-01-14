from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from django.db.models import Q
from django.http import Http404 
import random
# Create your views here.
from .models import products,variation,category

from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredMixin,LoginRequiredMixin


class CategoryListView(ListView):
	model=category
	queryset=category.objects.all()
	template_name="products/products_list.html"

class CategoryDetailView(DetailView):
	model=category

	def get_context_data(self,*args,**kwargs):
		context=super(CategoryDetailView,self).get_context_data(*args,**kwargs)
		obj=self.get_object()
		product_set=self.object.products_set.all()
		default_products=self.object.default_category.all()
		products=( product_set | default_products ).distinct()
		context["products"]=products
		return context	


class VariationListView(StaffRequiredMixin,ListView):
	model= variation
	queryset=variation.objects.all()
	def get_context_data(self,*args,**kwargs):
		context=super(VariationListView,self).get_context_data(*args,**kwargs)
		#context['now']=timezone.now()
		context['formset']=VariationInventoryFormSet(queryset=self.get_queryset())
		
		return context
	
	def get_queryset(self,*args,**kwargs):
		product_pk=self.kwargs.get("pk")
		if product_pk:
			product= get_object_or_404(products ,pk=product_pk)
			queryset=variation.objects.filter(products=product)
		return queryset

	def post(self, request,*args,**kwargs):
		#
		formset=VariationInventoryFormSet(request.POST,request.FILES)
		#print (request.POST)
		if formset.is_valid():
			formset.save(commit=False) 
			for form in formset:
				new_item=form.save(commit=False)
				if new_item.title:
					product_pk=self.kwargs.get('pk')
					product=get_object_or_404(products,pk=product_pk)
					new_item.product=product
					new_item.save()  
			
			messages.success(request,"your inventry and pricing has been updated")
			return redirect("Products")

		raise Http404



class ProductListView(ListView):
	model=products
	queryset=products.objects.filter(active=True)
	def get_context_data(self,*args,**kwargs):
		context=super(ProductListView,self).get_context_data(*args,**kwargs)
		context['now']=timezone.now()
		context['query']=self.request.GET.get("q")
		return context

	def get_queryset(self,*args,**kwargs):
		qs=super(ProductListView,self).get_queryset(*args,**kwargs)
		query=self.request.GET.get("q")
		if query:
			qs=self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)  
				)
		return qs




class ProductDetailView(DetailView):
	model=products
	def get_context_data(self,*args,**kwargs):
		context=super(ProductDetailView,self).get_context_data(*args,**kwargs)
		instance=self.get_object()
		context["related"]= sorted(products.objects.get_related(instance)[:4],key= lambda x:random.random())
		return context

def Product_Detail_View_fun(requests,id):
	Product_instance=products.objects.get(id=id)
	template="products/products_detail.html"
	context={
	"object":Product_instance

	}
	return render(requests,template,context)
