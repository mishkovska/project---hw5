from django.shortcuts import get_object_or_404, render
from .models import Category, Product

def home(request):
    categories_new_arrival = Category.objects.filter(is_new_arrival=True)

    context = {
        'categories_new_arrival': categories_new_arrival
    }

    return render(request, 'store/home.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)

    context = {
        'product': product
    }

    return render(request, 'store/products/detail.html', context)

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    descendants = category.get_descendants(include_self=True)

    products = Product.products.filter(category__in=descendants)

    root = category.get_root()
    if root.has_phone_type:
        if category.is_root_category():
            descendants = category.get_descendants().exclude(id__in=category.get_children().values_list('id', flat=True))
        else:
            if category.parent == root:
                descendants = category.get_descendants()
            else:
                descendants = category.get_descendants(include_self=True)
    else:
        descendants = []

    context = {
        'category': category,
        'products': products,
        'descendants': descendants
    }

    return render(request, 'store/products/category.html', context)




