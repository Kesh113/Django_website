# Generated by Django 5.0.2 on 2024-03-17 00:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0008_husband_test_app_husband'),
    ]

    operations = [
        migrations.AddField(
            model_name='husband',
            name='m_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='test_app',
            name='husband',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='woman', to='test_app.husband'),
        ),
    ]