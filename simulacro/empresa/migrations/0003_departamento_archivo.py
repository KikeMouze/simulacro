# Generated by Django 4.2.2 on 2024-03-09 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0002_alter_empleado_departamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='archivo',
            field=models.FileField(default=1, upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
