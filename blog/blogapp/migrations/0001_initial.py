# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.CharField(max_length=200)),
                ('comment_text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('picture', models.ImageField(null=True, upload_to=b'pics/%Y/%m/%d', blank=True)),
                ('pub_date', models.DateTimeField()),
                ('keywords', models.CharField(max_length=200, null=True, blank=True)),
                ('category', models.ManyToManyField(to='blogapp.Category')),
                ('comment', models.ManyToManyField(to='blogapp.Comment')),
            ],
        ),
    ]
