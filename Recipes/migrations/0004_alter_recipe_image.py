# Generated by Django 3.2.3 on 2021-06-02 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recipes', '0003_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, default='testCardImg.png', help_text='Вы можете прикрепить к своему рецепту картинку', null=True, upload_to='recipes/', verbose_name='Картинка рецепта'),
        ),
    ]
