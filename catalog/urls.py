from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, BlogListView,
    BlogDetailView, BlogCreateView, BlogUpdateView,
    BlogDeleteView, VersionCreateView, VersionUpdateView,
    MyProductsListView
)

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("my-products/", MyProductsListView.as_view(), name="my_products"),
    path("product/<int:pk>/", cache_page(60 * 15)(ProductDetailView.as_view()) if settings.CACHE_ENABLED else ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    
    path("version/create/", VersionCreateView.as_view(), name="version_create"),
    path("version/<int:pk>/update/", VersionUpdateView.as_view(), name="version_update"),
    
    path("blog/", BlogListView.as_view(), name="blog_list"),
    path("blog/create/", BlogCreateView.as_view(), name="blog_create"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog/<slug:slug>/update/", BlogUpdateView.as_view(), name="blog_update"),
    path("blog/<slug:slug>/delete/", BlogDeleteView.as_view(), name="blog_delete"),
]