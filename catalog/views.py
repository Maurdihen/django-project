from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Product, BlogPost, Version
from .forms import ProductForm, VersionForm


class ProductListView(ListView):
    model = Product
    template_name = "catalog/index.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['products']:
            product.active_version = Version.objects.filter(
                product=product, 
                is_current=True
            ).first()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_version'] = Version.objects.filter(
            product=self.object,
            is_current=True
        ).first()
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('index')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('index')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('index')

class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'
    success_url = reverse_lazy('index')

class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/version_form.html'
    success_url = reverse_lazy('index')

class BlogListView(ListView):
    model = BlogPost
    template_name = 'catalog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blog_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
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
            base_slug = slugify(new_blog.title)
            
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            new_blog.slug = slug
            new_blog.save()
            
        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'catalog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save(commit=False)
            if blog.title != self.get_object().title:
                base_slug = slugify(blog.title)
                slug = base_slug
                counter = 1
                while BlogPost.objects.filter(slug=slug).exclude(pk=blog.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                blog.slug = slug
            blog.save()
            
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', args=[self.object.slug])

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
    slug_url_kwarg = 'slug'