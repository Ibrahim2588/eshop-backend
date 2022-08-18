from django.urls import path

from . import views


urlpatterns = [
    path('product/', views.ProductListView.as_view(), name='all products'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product detail'),
    path('product/category/<slug:category>/', views.ProductCategoryView.as_view(), name='category products'),
    path('product/category/recomended/<slug:category>/', views.ProductCategoryRecomendedView.as_view(), name='category products recomended'),

    path('categories/', views.CategoryListView.as_view(), name='all categories'),


    path('order/', views.OrderListCreateView.as_view()),
    path('order/<int:pk>/', views.OrderUpdateDestroyView.as_view()),

    path('command/', views.CommandView.as_view(), name='command management'),
]
