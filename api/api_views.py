from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from api.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
    CommentCreateSerializer
)
from shop_app.models import Category, Product


class CategoryListAPIView(generics.ListAPIView):
    """ Вывод JSON модели Категория """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductPagination(PageNumberPagination):

    page_size = 2
    page_size_query_param = 'page_size'


class ProductAPIView(generics.ListAPIView):
    """ Вывод всех товаров с модели Product """

    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'price']

    def get_queryset(self):
        products = Product.objects.filter(available=True)
        return products


class ProductDetailAPIView(APIView):
    """ Вывод конкретного продукта """

    def get(self, request, pk):
        products = Product.objects.get(id=pk, available=True)
        serializer = ProductDetailSerializer(products)
        return Response(serializer.data)


class CommentCreateAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
        return Response(status=201)