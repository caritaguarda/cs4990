from django.contrib import admin

# Register your models here.
from .models import Item, Category

class ItemInline(admin.TabularInline):
    model = Item
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ItemInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item)