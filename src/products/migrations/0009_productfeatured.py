# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_products_fancy_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeatured',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('image', models.ImageField(upload_to=products.models.image_upload_to_featured)),
                ('title', models.CharField(blank=True, max_length=120, null=True)),
                ('text', models.CharField(blank=True, max_length=220, null=True)),
                ('text_right', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
