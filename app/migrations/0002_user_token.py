# Generated by Django 2.0.6 on 2018-06-26 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(default='', max_length=32),
        ),
    ]
