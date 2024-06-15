from django.shortcuts import render
from django.db.models import Q
from recipes.models import Recipe
from django.http import Http404
from utils.pagination import make_pagination
import os

PER_PAGE = 3

def home(request):
    recipes = Recipe.objects.filter(
        is_published = True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE )

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
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
            'recipes': page_obj,
            'pagination_range': pagination_range,
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

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
        
    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}"',
        'recipes': recipes,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&search={search_term}',
    })

