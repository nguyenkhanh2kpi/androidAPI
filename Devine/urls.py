from django.urls import path
from .views import *


app_name = 'Devine'

urlpatterns = [
    path('categories/', DivineCategoryList.as_view(), name='divine-category-list'),
    path('softwares/', DivineSoftwareList.as_view(), name='divine-software-list'),
    path('software/<int:pk>/', DivineSoftwareDetail.as_view(), name='divine-software-detail'),
    path('software/category/<int:category_id>/', DivineSoftwareListByCategory.as_view(), name='divine-software-bycategory'),
    path('comments/<int:product_id>/', DivineCommentList.as_view(), name='divine-comment-list'),
    path('comment/add/<int:pk>/',AddComment.as_view(), name='divine-comment-add'),
    path('cart/add/<int:pk>/', AddCart.as_view(), name='add-to-cart'),
    path('cart/', DivineCartView.as_view(), name='cart'),
    path('cart/sub/<int:pk>/', SubCart.as_view(), name='sub-from-cart'),
    path('order/list/', DivineOrderPurchased.as_view(), name='order-list'),
    path('order/', Order.as_view(), name='order'),
    path('orders/<int:order_id>/', DivineOrderView.as_view(), name='order-details'),
    path('purchased-keys/', PurchasedKeys.as_view(), name='purchased-keys')
]
