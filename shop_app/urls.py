from django.urls import path
from shop_app import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductList.as_view(),
         name="product_list"),
    path('products/', views.ProductFilterView.as_view(),
         name="product_filter"),
    path('category/<slug:category_slug>/',
         views.CategoryProductView.as_view(), name="category_product"),
    path('profile/<int:pk>/', views.ProfileView.as_view(),
         name="profile_view"),
    path('profile/<int:pk>/update/', views.ProfileEditView.as_view(),
         name="profile_edit"),
    path('<int:product_pk>/comment/<int:pk>/like/',
         views.AddLikeComment.as_view(), name="comment_like"),
    path('<int:product_pk>/comment/<int:pk>/dislike/',
         views.AddDislikeComment.as_view(), name="comment_dislike"),
    path('<slug:product_slug>/comment/delete/<int:pk>/',
         views.CommentDelete.as_view(), name="comment_delete"),
    path('comment/<int:pk>/', views.AddComment.as_view(), name="add_comment"),
    path('<slug:slug>/', views.ProductDetail.as_view(), name="product_detail"),
]

