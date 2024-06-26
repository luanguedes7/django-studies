from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="recipes-home"),
    path('recipes/search/', views.search, name='recipes-search'),
    path('recipes/category/<int:category_id>/',
        views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipes-recipe"),
] 