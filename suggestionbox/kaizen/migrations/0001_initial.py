# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import easy_thumbnails.fields
import userena.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'new', max_length=3, choices=[(b'2do', b'To Do'), (b'rev', b'In Review'), (b'imp', b'Implemented'), (b'den', b'Denied'), (b'new', b'New')])),
                ('category', models.ForeignKey(to='kaizen.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot', easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.', upload_to=userena.models.upload_to_mugshot, verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.', max_length=15, verbose_name='privacy', choices=[(b'open', 'Open'), (b'registered', 'Registered'), (b'closed', 'Closed')])),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
        ),
        migrations.AddField(
            model_name='idea',
            name='profile',
            field=models.ForeignKey(to='kaizen.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='idea',
            field=models.ForeignKey(to='kaizen.Idea'),
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(to='kaizen.Profile'),
        ),
    ]
