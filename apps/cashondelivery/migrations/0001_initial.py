# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-03 18:40
from __future__ import unicode_literals

import apps.cashondelivery.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashOnDeliveryTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=128, verbose_name='Order Number')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Amount')),
                ('currency', models.CharField(blank=True, max_length=8, null=True, verbose_name='Currency')),
                ('reference', models.CharField(blank=True, default=apps.cashondelivery.models._make_uuid, max_length=100, unique=True, verbose_name='Reference')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Confirmed')),
                ('date_confirmed', models.DateTimeField(auto_now=True, verbose_name='Date Confirmed')),
            ],
            options={
                'verbose_name': 'Cash on Delivery',
                'ordering': ('-date_created',),
            },
        ),
    ]
