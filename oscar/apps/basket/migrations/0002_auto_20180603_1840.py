# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-03 18:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0001_initial'),
        ('partner', '0001_initial'),
        ('basket', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lineattribute',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Option', verbose_name='Option'),
        ),
        migrations.AddField(
            model_name='line',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='basket.Basket', verbose_name='Basket'),
        ),
        migrations.AddField(
            model_name='line',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='catalogue.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='line',
            name='stockrecord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_lines', to='partner.StockRecord'),
        ),
        migrations.AddField(
            model_name='basket',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='baskets', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]
