# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('description', models.TextField()),
                ('target_groups', models.CharField(max_length=50)),
                ('send_reminder', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CapstoneProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=-1, choices=[(-1, b'NOT STARTED'), (0, b'PROPOSAL'), (1, b'PART ONE'), (2, b'PART TWO'), (3, b'COMPLETED')])),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=100)),
                ('date_started', models.DateField()),
                ('date_ended', models.DateField()),
                ('status', models.IntegerField(default=-1, choices=[(-1, b'NOT STARTED'), (0, b'PREPARATION'), (1, b'AT POST'), (2, b'COMPLETED')])),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('middle_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('datetime_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageScheduler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sch_date', models.DateField()),
                ('sch_time', models.TimeField()),
                ('message', models.ForeignKey(to='info_system.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('speaker', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('academic_year', models.CharField(max_length=20)),
                ('semester', models.IntegerField(choices=[(1, b'First'), (2, b'Second')])),
                ('school', models.IntegerField(choices=[(1, b'SATES (Engineering)'), (2, b'ABS (Business)'), (3, b'ASDASS (IT/Computer Science)')])),
                ('seminar_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SeminarAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('authorized_by', models.ForeignKey(to='info_system.Manager')),
                ('seminar', models.ForeignKey(to='info_system.Seminar')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('middle_name', models.CharField(max_length=100, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('CDES_passed', models.BooleanField(default=False)),
                ('UFS_passed', models.BooleanField(default=False)),
                ('scadiil_level', models.IntegerField(default=0)),
                ('program', models.IntegerField(choices=[(1, b'SATES (Engineering)'), (2, b'ABS (Business)'), (3, b'ASDASS (IT/Computer Science)')])),
                ('capstone', models.ForeignKey(blank=True, to='info_system.CapstoneProject', null=True)),
                ('internship', models.ForeignKey(blank=True, to='info_system.Internship', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='seminarattendance',
            name='student',
            field=models.ForeignKey(to='info_system.Student'),
        ),
        migrations.AddField(
            model_name='capstoneproject',
            name='supervisor',
            field=models.ForeignKey(to='info_system.Supervisor'),
        ),
    ]
