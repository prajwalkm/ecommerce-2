from django.contrib import admin

# Register your models here.
from .models import products,variation,ProductImage,category,ProductFeatured

class ProductImageInLine(admin.TabularInline):
	model=ProductImage
	extra=0

class VariationInLine(admin.TabularInline):
	model=variation
	extra=0

class ProductAdmin(admin.ModelAdmin):
	list_display=['__str__','price']
	inlines=[ProductImageInLine,
	VariationInLine,
	


	]
	class Meta:
		model=products


admin.site.register(products,ProductAdmin)
admin.site.register(variation)
admin.site.register(ProductImage)
admin.site.register(category)
admin.site.register(ProductFeatured)