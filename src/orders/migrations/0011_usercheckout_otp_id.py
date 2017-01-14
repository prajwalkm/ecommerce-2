# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20161208_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercheckout',
            name='otp_id',
            field=models.CharField(null=True, max_length=120, blank=True),
        ),
    ]
