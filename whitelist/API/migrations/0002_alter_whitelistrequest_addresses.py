# Generated by Django 4.2.9 on 2024-01-05 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whitelistrequest',
            name='addresses',
            field=models.TextField(blank=True, null=True),
        ),
    ]
