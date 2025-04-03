from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, "catalog/index.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})