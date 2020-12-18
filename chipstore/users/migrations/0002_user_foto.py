# Generated by Django 3.0.11 on 2020-12-15 21:20

import chipstore.utils.common
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='foto',
            field=models.ImageField(default='/', upload_to=chipstore.utils.common.get_image_directory_path),
            preserve_default=False,
        ),
    ]
