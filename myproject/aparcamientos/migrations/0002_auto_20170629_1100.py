# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aparcamiento',
            name='latitud',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='aparcamiento',
            name='longitud',
            field=models.FloatField(default=0),
        ),
    ]
