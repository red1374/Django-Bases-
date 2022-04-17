from django.urls import path
from .views import ProductListView, ProductView

app_name = 'products'

urlpatterns = [
   path('', ProductListView.as_view(), name='index'),
   path('category/<int:pk>/', ProductListView.as_view(), name='category'),
   path('category/<int:pk>/page/<int:page>/', ProductListView.as_view(), name='page'),
   path('product/<int:pk>/', ProductView.as_view(), name='product')
]
