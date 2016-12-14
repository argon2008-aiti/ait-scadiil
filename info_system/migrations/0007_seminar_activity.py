# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_system', '0006_auto_20160920_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminar',
            name='activity',
            field=models.OneToOneField(default=1, to='info_system.Activity'),
            preserve_default=False,
        ),
    ]
