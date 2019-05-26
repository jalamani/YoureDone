from django.urls import path

from . import views

app_name = 'foodlog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:foodlist_id>/', views.detail, name='detail'),
    path('<int:foodlist_id>/', views.addFood, name='addFood'),
]