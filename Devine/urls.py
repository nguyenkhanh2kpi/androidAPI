from django.urls import path
from .views import *


app_name = 'Devine'

urlpatterns = [
    path('categories/', DivineCategoryList.as_view(), name='divine-category-list'),
    path('softwares/', DivineSoftwareList.as_view(), name='divine-software-list'),
    path('software/<int:pk>', DivineSoftwareDetail.as_view(), name='divine-software-detail'),
    path('software/category/<int:category_id>', DivineSoftwareListByCategory.as_view(), name='divine-software-bycategory'),
    path('comments/<int:product_id>', DivineCommentList.as_view(), name='divine-comment-list'),
    path('comment/add/<int:pk>',AddComment.as_view(), name="divine-comment-add"),

]
