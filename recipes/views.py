from django.shortcuts import render
from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404

def home(request):
    recipes = Recipe.objects.filter(
        is_published = True,
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
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
    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}"'
    })