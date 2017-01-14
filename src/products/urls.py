from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import ProductDetailView,ProductListView,VariationListView
urlpatterns = [
    # Examples:
   # url(r'^$', 'newsletter.views.home', name='home'),
   #url(r'^(?P<id>\d+)', 'products.views.Product_Detail_View_fun', name='Product_Detail_function'),
   url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='ProductsDetail'),
   url(r'^$', ProductListView.as_view(), name='Products'),
   url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='product_inventory'),    
]