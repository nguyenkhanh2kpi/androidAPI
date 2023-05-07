from django.urls import path
from .views import *


app_name = 'Devine'

urlpatterns = [
    path('categories/', DivineCategoryList.as_view(), name='divine-category-list'),
    path('softwares/', DivineSoftwareList.as_view(), name='divine-software-list'),
    path('software/<int:pk>/', DivineSoftwareDetail.as_view(), name='divine-software-detail'),
    path('keys/', DivineKeyList.as_view(), name='divine-key-list'),
    path('comments/', DivineCommentList.as_view(), name='divine-comment-list'),
]
