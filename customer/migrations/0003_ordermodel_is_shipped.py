# Generated by Django 5.0.7 on 2024-09-15 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_ordermodel_city_ordermodel_email_ordermodel_is_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]