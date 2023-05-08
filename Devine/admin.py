from django.contrib import admin
from .models import *


class DivineCartItemInline(admin.TabularInline):
    model = DivineCartItem
    extra = 0
    fields = ['software', 'quantity']

class DivineOrderDetailInline(admin.TabularInline):
    model = DivineOrderDetail


@admin.register(DivineCategory)
class DivineCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineSoftware)
class DivineSoftwareAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'quantity']

@admin.register(DivineKey)
class DivineKeyAdmin(admin.ModelAdmin):
    list_display = ['software', 'key_code', 'is_used']

@admin.register(DivineOrder)
class DivineOrderAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    inlines = [DivineOrderDetailInline]


@admin.register(DivineOrderDetail)
class DivineOrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id','key','quantity']

@admin.register(DivineComment)
class DivineCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']

@admin.register(DivineCart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user']
    inlines = [DivineCartItemInline]


@admin.register(DivineCartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['software','quantity']
