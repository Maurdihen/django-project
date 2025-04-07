from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Product, BlogPost

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "catalog/index.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

class BlogListView(ListView):
    model = BlogPost
    template_name = 'catalog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Выводим только опубликованные статьи
        return BlogPost.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blog_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        # Увеличиваем счетчик просмотров
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj

class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'catalog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save(commit=False)
            # Генерируем slug из заголовка
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'catalog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('blog_detail', args=[self.object.slug])

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
    slug_url_kwarg = 'slug'