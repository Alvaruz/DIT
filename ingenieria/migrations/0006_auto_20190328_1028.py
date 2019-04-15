# Generated by Django 2.1.7 on 2019-03-28 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieria', '0005_documento_creado_por'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='creado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='generado_por', to=settings.AUTH_USER_MODEL),
        ),
    ]
