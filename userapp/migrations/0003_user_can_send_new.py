# Generated by Django 3.2.5 on 2021-08-11 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_auto_20210810_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_send_new',
            field=models.BooleanField(default=True),
        ),
    ]
