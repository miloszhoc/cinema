# Generated by Django 3.0.4 on 2020-04-04 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0042_tickettype_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='media/images/'),
        ),
    ]
