from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()


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
