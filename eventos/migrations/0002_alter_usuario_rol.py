# Generated by Django 5.0.6 on 2024-07-05 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('admin', 'Administrador'), ('normal', 'Usuario Normal')], default='normal', max_length=7),
        ),
    ]