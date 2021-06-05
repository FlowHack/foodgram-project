from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from Recipes.models import Recipe


class RecipeAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Recipe
        exclude = ['pub_date']


class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Recipe
        exclude = ['pub_date', 'slug', 'author', 'tag', 'ingredients']
