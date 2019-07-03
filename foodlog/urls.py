from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'foodlog'
urlpatterns = [
	path('users/', views.users, name='users'),
    path('index/', views.index, name='index'),
    path('<int:foodlist_id>/', views.detail, name='detail'),
    path('delete/<int:pk>/', views.foodlist_delete, name='foodlist_delete'),
    path('<int:foodlist_id>/<int:food_id>/', views.food_delete, name='food_delete')
]