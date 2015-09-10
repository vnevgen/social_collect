# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PersonAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=20, choices=[('twitter', 'Twitter'), ('vk', 'VKontakte'), ('instagram', 'Instagram')])),
                ('screen_name', models.CharField(max_length=255)),
                ('social_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('image', models.CharField(max_length=255, blank=True)),
                ('use_image', models.BooleanField(default=False)),
                ('person', models.ForeignKey(related_name='accounts', to='social_collect.Person')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='personaccount',
            unique_together=set([('type', 'social_id')]),
        ),
    ]
