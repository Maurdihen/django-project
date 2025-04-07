from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    BlogListView, BlogDetailView, BlogCreateView,
    BlogUpdateView, BlogDeleteView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    
    # URLs для блога
    path("blog/", BlogListView.as_view(), name="blog_list"),
    path("blog/create/", BlogCreateView.as_view(), name="blog_create"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog/<slug:slug>/update/", BlogUpdateView.as_view(), name="blog_update"),
    path("blog/<slug:slug>/delete/", BlogDeleteView.as_view(), name="blog_delete"),
]