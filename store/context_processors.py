from .models import Category

def categories(request):
    return {
        'categories_in_menu': Category.objects.filter(is_displayed_in_menu=True)
    }