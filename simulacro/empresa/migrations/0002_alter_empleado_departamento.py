# Generated by Django 5.0.3 on 2024-03-09 16:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='departamento',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='empresa.departamento'),
        ),
    ]