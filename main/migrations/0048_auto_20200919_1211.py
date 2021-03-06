# Generated by Django 3.1 on 2020-09-19 19:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0047_auto_20200918_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='last_message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
