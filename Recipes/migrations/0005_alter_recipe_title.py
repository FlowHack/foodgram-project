# Generated by Django 3.2.3 on 2021-06-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes', '0004_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(help_text='Введите название рецепта', max_length=50, verbose_name='Название'),
        ),
    ]
