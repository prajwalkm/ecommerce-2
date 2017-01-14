# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20161120_0721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='mobile_number',
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(to='carts.Cart', null=True),
        ),
    ]
