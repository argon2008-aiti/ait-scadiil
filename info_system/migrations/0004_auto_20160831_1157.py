# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_system', '0003_seminarattendance_venue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seminar',
            name='academic_year',
        ),
        migrations.RemoveField(
            model_name='seminar',
            name='semester',
        ),
    ]
