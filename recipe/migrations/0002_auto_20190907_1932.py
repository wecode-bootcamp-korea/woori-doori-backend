# Generated by Django 2.2.4 on 2019-09-07 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_no',
            new_name='category_number',
        ),
        migrations.RenameField(
            model_name='categoryitem',
            old_name='item_no',
            new_name='item_number',
        ),
        migrations.RenameField(
            model_name='recipeitem',
            old_name='categoryItem',
            new_name='category_item',
        ),
    ]