# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(to='blogapp.Category', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='comment',
            field=models.ManyToManyField(to='blogapp.Comment', null=True, blank=True),
        ),
    ]
