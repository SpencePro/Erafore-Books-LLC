# Generated by Django 3.2.5 on 2021-09-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_loreobject_series'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='audio_book',
            field=models.BooleanField(default=False),
        ),
    ]