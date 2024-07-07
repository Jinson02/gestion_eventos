# Generated by Django 5.0.6 on 2024-07-07 06:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_rename_descripcion_evento_descripción_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='creador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]