# Generated by Django 4.0 on 2022-01-27 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_notebook_ispublic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notebook',
            name='id',
        ),
        migrations.AddField(
            model_name='notebook',
            name='shareList',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notebook',
            name='slug',
            field=models.CharField(max_length=25, primary_key=True, serialize=False),
        ),
    ]