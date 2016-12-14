# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_system', '0002_auto_20160816_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminarattendance',
            name='venue',
            field=models.CharField(default='Seaview Campus(EBL-31)', max_length=100),
            preserve_default=False,
        ),
    ]
