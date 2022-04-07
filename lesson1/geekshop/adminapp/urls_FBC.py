from django.urls import path, re_path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.main, name='main'),

    re_path(r'^users/read/page/(?P<page>[0-9])/$', adminapp.users, name='users_page'),
    path('users/read/', adminapp.users, name='users'),
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    re_path(r'^categories/read/page/(?P<page>[0-9])/$', adminapp.categories, name='categories_page'),
    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/update/<int:pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),
    path('categories/read/', adminapp.categories, name='categories'),

    re_path(r'^products/read/category/(?P<pk>[0-9])/page/(?P<page>[0-9])/$', adminapp.products, name='products_page'),
    path('products/read/<int:pk>/', adminapp.product_read, name='product_read'),
    path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    path('products/create/category/<int:pk>/', adminapp.product_create, name='product_create'),
    path('products/update/<int:pk>/', adminapp.product_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.product_delete, name='product_delete'),
]
