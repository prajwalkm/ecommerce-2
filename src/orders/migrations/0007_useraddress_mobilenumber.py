# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20161115_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='mobileNumber',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
    ]
