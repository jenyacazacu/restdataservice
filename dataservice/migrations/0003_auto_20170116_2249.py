# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 22:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataservice', '0002_auto_20170116_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeddata',
            name='file',
        ),
        migrations.DeleteModel(
            name='StoredData',
        ),
    ]
