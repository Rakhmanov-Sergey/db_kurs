# Generated by Django 2.2.7 on 2019-11-19 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_event_songs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='songs',
            field=models.ManyToManyField(blank=True, null=True, to='core.Song'),
        ),
    ]
