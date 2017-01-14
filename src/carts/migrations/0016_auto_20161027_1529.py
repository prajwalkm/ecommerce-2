# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0015_auto_20161027_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='taxpercent',
            field=models.DecimalField(max_digits=50, decimal_places=5, default=0.0),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(to='carts.Cart'),
        ),
    ]
