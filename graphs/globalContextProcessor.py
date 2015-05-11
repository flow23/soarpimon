from .models import Graph

def graphCategories(request):
    return {
        'categories': Graph._meta.get_field('category').choices,
    }
