# Generated by Django 2.2.7 on 2019-11-15 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
