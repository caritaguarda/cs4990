# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='name',
            field=models.CharField(default='None', max_length=200),
            preserve_default=False,
        ),
    ]
