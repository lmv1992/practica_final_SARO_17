# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamiento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.TextField(default='')),
                ('descripcion', models.TextField(default='')),
                ('accessibilidad', models.IntegerField(default='')),
                ('url', models.TextField(default='')),
                ('barrio', models.TextField(default='')),
                ('distrito', models.TextField(default='')),
                ('latitud', models.FloatField(default='')),
                ('longitud', models.FloatField(default='')),
                ('cuantidad_likes', models.IntegerField(default=0)),
                ('numero_comentarios', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AparcamientoSeleccionado',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('aparcamiento', models.ForeignKey(to='aparcamientos.Aparcamiento')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('anotacion', models.TextField(default='')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('aparcamiento', models.ForeignKey(default='', to='aparcamientos.Aparcamiento')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaginaUsuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('titulo', models.TextField(default='Página de ususario')),
                ('color', models.CharField(max_length=32, default='#e9dede')),
                ('tamanho', models.IntegerField(default=12)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
