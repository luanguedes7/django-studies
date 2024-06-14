from django.shortcuts import render
from django.db.models import Q
from recipes.models import Recipe
from django.http import Http404
from django.core.paginator import Paginator
from utils.pagination import make_pagination_range

def home(request):
    recipes = Recipe.objects.filter(
        is_published = True,
    ).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(recipes, 3)
    page_obj = paginator.get_page(current_page)
    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
    })

def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published = True,
    ).order_by('-id')

    if not recipes:
        raise Http404('Not found! :(')

    return render(request, 'recipes/pages/category.html', context={
            'recipes': recipes,
            'title': f'{recipes.first().category.name} - Category' 
    })

def recipe(request, id):
    recipe = Recipe.objects.filter(
        pk=id,
        is_published = True,
    ).order_by('-id').first()

    if not recipe:
        raise Http404('Not found! :(')

    return render(request, 'recipes/pages/recipe-template.html', context={
        'recipe':recipe,
        'is_detail_page': True
    })

def search(request):
    search_term = request.GET.get('search', '').strip()

    if not search_term:
        raise Http404
    
    recipes = Recipe.objects.filter(
          Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')
        
    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}"',
        'recipes': recipes,
    })

