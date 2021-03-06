# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-29 12:10
from __future__ import unicode_literals

import company.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20170927_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblcoupons',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tblvendor',
            name='cover_photo',
            field=models.FileField(blank=True, null=True, upload_to=company.models.get_vendor_image_path),
        ),
    ]
