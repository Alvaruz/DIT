# Generated by Django 2.1.7 on 2019-04-01 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingenieria', '0006_auto_20190328_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='creado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='generado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documento',
            name='recurrente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ingenieria.Recurrente'),
        ),
    ]
