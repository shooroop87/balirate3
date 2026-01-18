from django.urls import path
from . import views

app_name = 'developers'

urlpatterns = [
    path('', views.developer_list, name='list'),
    path('<slug:slug>/', views.developer_detail, name='detail'),
]