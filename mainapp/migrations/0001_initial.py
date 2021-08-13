# Generated by Django 3.2.5 on 2021-08-10 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_started', models.DateField()),
                ('world', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoreObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('world', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.series')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('synopsis', models.TextField()),
                ('cover_artist', models.CharField(blank=True, max_length=255, null=True)),
                ('date_released', models.DateField()),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('amazon_link', models.URLField(blank=True, max_length=255, null=True)),
                ('world', models.CharField(blank=True, max_length=255, null=True)),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.series')),
            ],
        ),
    ]
