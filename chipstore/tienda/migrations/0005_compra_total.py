# Generated by Django 3.0.11 on 2020-12-20 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0004_auto_20201219_0410'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='total',
            field=models.FloatField(null=True),
        ),
    ]