# Generated by Django 3.2.13 on 2023-03-27 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20230326_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='affective',
            name='module',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='student.module'),
            preserve_default=False,
        ),
    ]
