from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from Recipes.models import Recipe


class RecipeAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Recipe
        exclude = ['pub_date']
