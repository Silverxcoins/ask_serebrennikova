# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0002_auto_20151126_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='value',
            new_name='like_type',
        ),
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]
