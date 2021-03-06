# Generated by Django 3.2.6 on 2021-09-01 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0005_auto_20210901_0525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line1',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='post_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='town_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
