# Generated by Django 3.1.4 on 2021-01-03 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebook',
            name='slug',
            field=models.CharField(default='Add slug', max_length=25),
            preserve_default=False,
        ),
    ]
