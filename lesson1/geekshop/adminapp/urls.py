from django.urls import path, re_path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.main, name='main'),

    re_path(r'^users/read/page/(?P<page>[0-9])/$', adminapp.UsersListView.as_view(), name='users_page'),
    path('users/read/', adminapp.UsersListView.as_view(), name='users'),
    path('users/create/', adminapp.UsersCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', adminapp.UsersUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UsersDeleteView.as_view(), name='user_delete'),

    re_path(r'^categories/read/page/(?P<page>[0-9])/$', adminapp.ProductCategoryListView.as_view(),
            name='categories_page'),
    path('categories/read/', adminapp.ProductCategoryListView.as_view(), name='categories'),
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),

    path('products/read/category/<int:pk>/', adminapp.ProductListView.as_view(), name='products'),
    re_path(r'^products/read/category/(?P<pk>[0-9])/page/(?P<page>[0-9])/$', adminapp.ProductListView.as_view(), name='products_page'),
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('products/create/category/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
]
