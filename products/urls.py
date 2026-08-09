from django.urls import path
from .views import (
    ProductDetailView,
    ProductListCreateView,
    ProductPurchaseView,
)


urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path(
        'products/<int:pk>/purchase/',
        ProductPurchaseView.as_view(),
        name='product-purchase'
    ),
]