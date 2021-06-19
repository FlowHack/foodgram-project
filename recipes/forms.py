from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Recipe
        exclude = ['pub_date']


class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    tag = forms.ModelMultipleChoiceField(
        required=True, queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Recipe
        exclude = ['pub_date', 'slug', 'author', 'ingredients']
