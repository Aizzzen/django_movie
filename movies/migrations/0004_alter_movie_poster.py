# Generated by Django 4.2.2 on 2023-06-18 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movie_premiere'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(upload_to='movies/', verbose_name='Постер'),
        ),
    ]
