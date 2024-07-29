from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product, name='product'),
    path('carts/', views.carts, name='carts'),
    path('users/', views.users, name='users'),
    path('tour/', views.tour, name='tour'),
    path('operator_filter/', views.operator_filter, name='operator_filter'),
    path('page=<int:page_number>/', views.page, name='page'),
    path('days/', views.days, name='days'),
    path('group_size/', views.group_size, name='group_size')
]
