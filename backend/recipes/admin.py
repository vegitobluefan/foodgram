from django.contrib import admin
from django.utils.html import format_html

from .models import (FavoriteRecipe, Ingredient, MyUser, Recipe, ShoppingCart,
                     SubscriptionUser, Tag)

admin.site.register(SubscriptionUser)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCart)
admin.site.register(Tag)


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'recipe_favorite',)
    search_fields = ('name', 'author',)

    @admin.display(
        description=format_html('<strong>Рецепт в избранных</strong>'))
    def recipe_favorite(self, Recipe):
        return Recipe.favorite_recipe.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
