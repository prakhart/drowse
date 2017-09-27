# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-27 13:29
from __future__ import unicode_literals

import company.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20170927_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblvendor',
            name='cover_photo',
            field=models.FileField(blank=True, null=True, upload_to=company.models.get_vendor_image_path),
        ),
    ]
