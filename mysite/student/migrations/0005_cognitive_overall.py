# Generated by Django 3.2.13 on 2023-03-26 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20230326_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='cognitive',
            name='overall',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3),
        ),
    ]
