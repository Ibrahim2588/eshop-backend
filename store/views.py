from django.http import Http404
from django.shortcuts import get_object_or_404, render
from requests import request

from .models import (
    Order,
    Category,
    Product,
    Characteristics,
    Image,
)
from .serializers import (
    OrderSerializer,
    CategorySerialiser,
    ProductListSerializer,
    ProductDetailSerializer
)

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import (
    mixins,
    generics,
    views,
    viewsets,
    status,
    authentication,
    permissions,
    pagination,
    parsers,
    filters
)



class Pagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    # max_page_size = 3

class ProductListView(generics.ListAPIView,):
    queryset = Product.objects.filter(is_avtivated=True)
    serializer_class = ProductListSerializer
    # pagination_class = Pagination
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = [
        'title',
        'description',
    ]



class AbstractProductCategory(generics.ListAPIView):
    queryset = Product.objects.filter(is_avtivated=True)
    serializer_class = ProductListSerializer
    pagination_class = Pagination

    class Meta: 
        abstract = True

class ProductCategoryView(AbstractProductCategory):
    def get_queryset(self):
        category_slug = self.kwargs['category']
        query = super().get_queryset()
        return query.filter(category__value=category_slug).order_by('title')

class ProductCategoryRecomendedView(AbstractProductCategory):
    def get_queryset(self):
        category_slug = self.kwargs['category']
        query = super().get_queryset()
        return query.filter(
            category__value=category_slug,
            recomended=True    
        )


# @api_view(['GET', ])
# def ProductCategoryView(request, category_slug):

#     if request.method == 'GET':
        
#         products = Product.objects.filter(category__value=category_slug)
#         products_data = ProductListSerializer(products, many=True).data
#         return Response(products_data, status.HTTP_200_OK)

#     return Response(f'method {request.method} not allowed')
        


class ProductDetailView(generics.RetrieveAPIView,):
    queryset = Product.objects.filter(is_avtivated=True)
    serializer_class = ProductDetailSerializer

class CategoryListView(
    generics.ListAPIView,
    generics.RetrieveAPIView,
    ):
    queryset = Category.objects.all()
    serializer_class = CategorySerialiser
    lookup_field = 'value'


class OrderListCreateView(
    generics.ListCreateAPIView,
    ):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    # authentication_classes = [
    #     authentication.TokenAuthentication
    # ]

    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

class OrderUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView,
    ):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    # authentication_classes = [
    #     authentication.TokenAuthentication
    # ]

    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(user=self.request.user)
