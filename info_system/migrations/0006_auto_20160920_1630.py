# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_system', '0005_remove_seminarattendance_venue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='send_reminder',
        ),
        migrations.AlterField(
            model_name='activity',
            name='target_school',
            field=models.IntegerField(choices=[(1, b'SATES (Engineering)'), (2, b'ABS (Business)'), (3, b'ASDASS (IT/Computer Science)')]),
        ),
    ]
