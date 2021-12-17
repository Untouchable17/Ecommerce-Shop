from django.urls import path

from api import api_views

urlpatterns = [
    path('categories/', api_views.CategoryListAPIView.as_view(),
         name="api_categories"),
    path('products/', api_views.ProductAPIView.as_view(),
         name="api_products"),
    path('product/<int:pk>/', api_views.ProductDetailAPIView.as_view(),
         name="api_product_detail"),
    path('comment/', api_views.CommentCreateAPIView.as_view(),
         name="api_comment"),
]
