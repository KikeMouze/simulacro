# Generated by Django 4.2.2 on 2024-03-10 20:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0003_departamento_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='campo_fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='archivo',
            field=models.FileField(upload_to='media/uploads/'),
        ),
    ]
