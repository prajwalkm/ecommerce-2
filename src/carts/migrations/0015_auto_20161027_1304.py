# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0014_auto_20161024_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='taxtotal',
            field=models.DecimalField(decimal_places=2, max_digits=50, default=0.0),
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=50, default=0.0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, max_digits=50, default=0.0),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(to='carts.Cart'),
        ),
    ]
