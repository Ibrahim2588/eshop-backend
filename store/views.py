from django.http import Http404
from django.shortcuts import get_object_or_404, render
from requests import request

from .models import (
    Command,
    Order,
    Category,
    Product,
    Characteristics,
    Image,
)
from .serializers import (
    CommandSerializer,
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
    page_size = 2
    page_size_query_param = 'page_size'
    # max_page_size = 3


class ProductListView(generics.ListAPIView,):
    queryset = Product.objects.filter(is_avtivated=True)
    serializer_class = ProductListSerializer
    # pagination_class = Pagination
    filter_backends = [
        filters.SearchFilter,
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
        return query.filter(category__value=category_slug)


class ProductCategoryRecomendedView(AbstractProductCategory):
    def get_queryset(self):
        category_slug = self.kwargs['category']
        query = super().get_queryset()
        return query.filter(
            category__value=category_slug,
            recomended=True,
        )

class BestProductListView(generics.ListAPIView,):
    queryset = Product.objects.filter(is_avtivated=True)
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        query = super().get_queryset()
        return query


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
    queryset = Order.objects.filter(is_active=True)
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
    queryset = Order.objects.filter(is_active=True)
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



class CommandView(generics.ListCreateAPIView):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    
    def get_queryset(self):
        query = super().get_queryset()
        return query.filter(user=self.request.user)


    def post(self, request, *args, **kwargs):
        print(request.data)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        command = serializer.save(
            user=user,
            command_code=command_code()
        )

        orders = Order.objects.filter(user=user, is_active=True)
        for order in orders:
            order.command = command
            order.ordered = True
            order.is_active = False
            order.save()

@api_view(['POST', 'GET', ])
def _CommandView(request):
    
    if request.user.is_authenticated:

        user = request.user
        commands = Command.objects.filter(user=user)
        orders = Order.objects.filter(user=user).prefetch_related('product')

        if request.method == 'POST':
            command = CommandSerializer(data=request.data)
            if command.is_valid(raise_exception=True):
                command.user = request.user
                command.command_code = command_code()
                command.save()

                orders.command = command
                orders.save()
                
            return Response(command, 200)
            
        if request.method == 'GET':
            commands_data = CommandSerializer(commands, many=True).data

            return Response(commands_data, status.HTTP_200_OK)
        

    else:
        return Response({'details': 'user must be authenticated'}, status.HTTP_200_OK)



def command_code():
    from random import  randint

    chars = [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'W',
        'Z',
    ]

    chars1 = []
    chars2 = []
    chars3 = []

    for i in range(3):
        chars1.append(chars[randint(0, 35)])

    for i in range(4):
        chars2.append(chars[randint(0, 35)])

    for i in range(3):
        chars3.append(chars[randint(0, 35)])


    one = ''.join(chars1)
    two = ''.join(chars2)
    thre = ''.join(chars3)

    code = '-'.join([one, two, thre])

    return str(code)