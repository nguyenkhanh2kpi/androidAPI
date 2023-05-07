from django.contrib import admin
from .models import *

@admin.register(DivineCategory)
class DivineCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineSoftware)
class DivineSoftwareAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineKey)
class DivineKeyAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineOrder)
class DivineOrderAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineOrderDetail)
class DivineOrderDetailAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineComment)
class DivineCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineCart)
class CartAdmin(admin.ModelAdmin):
    pass

@admin.register(DivineCartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
