from rest_framework import generics, pagination
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


class ProductPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.all().order_by('id')

        search = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if search:
            queryset = queryset.filter(name__icontains=search)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductPurchaseView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, pk):
        product = self.get_object()

        quantity = request.data.get('quantity')

        if not quantity:
            return Response(
                {'error': 'Quantity is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {'error': 'Quantity must be a valid number.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity <= 0:
            return Response(
                {'error': 'Quantity must be greater than 0.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > product.stock:
            return Response(
                {'error': 'Insufficient stock.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.stock -= quantity
        product.save()

        return Response(ProductSerializer(product).data)