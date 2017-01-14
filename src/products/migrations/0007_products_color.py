# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_products_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='color',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
    ]
