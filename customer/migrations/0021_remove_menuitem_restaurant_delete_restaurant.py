# Generated by Django 5.0.7 on 2024-11-09 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_restaurant_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='restaurant',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]