# Generated by Django 3.1 on 2020-09-14 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20200913_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_traded',
            field=models.DateField(blank=True),
        ),
    ]
