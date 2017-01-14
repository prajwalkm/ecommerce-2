# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20161013_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='gender',
            field=models.CharField(max_length=120, choices=[('mens', 'Mens'), ('ladies', 'Ladies')], default='Mens'),
        ),
    ]
