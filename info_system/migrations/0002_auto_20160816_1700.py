# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seminar',
            name='seminar_number',
        ),
        migrations.AddField(
            model_name='activity',
            name='target_school',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='capstoneproject',
            name='part_one_mark',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='capstoneproject',
            name='part_two_mark',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='internship',
            name='status',
            field=models.IntegerField(default=-1, choices=[(-1, b'NOT STARTED'), (0, b'PREPARATION'), (1, b'AT POST'), (2, b'RETURNEE'), (3, b'COMPLETED')]),
        ),
    ]
