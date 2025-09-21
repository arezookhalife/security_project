from django.urls import path
from .views import edit_product, ProductDetailView

urlpatterns = [
    path('products/<int:product_id>/edit/', edit_product, name='edit_product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
