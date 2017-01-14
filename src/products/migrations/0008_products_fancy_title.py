# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_products_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='fancy_title',
            field=models.CharField(default='Trendy Watch', max_length=120),
        ),
    ]
