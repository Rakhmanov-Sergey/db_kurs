# Generated by Django 2.2.7 on 2019-11-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20191119_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='songs',
            field=models.ManyToManyField(to='core.Song'),
        ),
    ]
