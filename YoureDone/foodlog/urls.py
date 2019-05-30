from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'foodlog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:foodlist_id>/', views.detail, name='detail'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.foodlist_delete, name='foodlist_delete')
]