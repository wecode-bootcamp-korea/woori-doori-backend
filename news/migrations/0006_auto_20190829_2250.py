# Generated by Django 2.2.4 on 2019-08-29 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20190829_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]
