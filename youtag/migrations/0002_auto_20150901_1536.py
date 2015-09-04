# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youtag', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagvideo',
            name='tag',
        ),
        migrations.AddField(
            model_name='tagvideo',
            name='tags',
            field=models.ManyToManyField(to='youtag.Tag'),
        ),
    ]
