# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('word', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TagVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('tag', models.ForeignKey(to='youtag.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('vidId', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=400)),
                ('desc', models.CharField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='tagvideo',
            name='video',
            field=models.ForeignKey(to='youtag.Video'),
        ),
    ]
