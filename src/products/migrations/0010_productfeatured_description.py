# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_productfeatured'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeatured',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
