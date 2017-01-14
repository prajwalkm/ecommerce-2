# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_useraddress_mobilenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mobile_number',
            field=models.ForeignKey(null=True, related_name='mobile_number', to='orders.UserAddress'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(to='carts.Cart'),
        ),
    ]
