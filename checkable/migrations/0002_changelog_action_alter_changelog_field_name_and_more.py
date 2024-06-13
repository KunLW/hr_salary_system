# Generated by Django 5.0.6 on 2024-06-13 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='changelog',
            name='action',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='changelog',
            name='field_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='new_value',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='changelog',
            name='old_value',
            field=models.TextField(blank=True, null=True),
        ),
    ]