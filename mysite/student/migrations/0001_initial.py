# Generated by Django 3.2.13 on 2023-03-26 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True, verbose_name='Module Code')),
                ('name', models.CharField(max_length=30, verbose_name='First name')),
                ('week', models.IntegerField(default=0)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ca_weight', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('exam_weight', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.module')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Cognitive',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('coursework', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('exam', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.module')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Behavioural',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.module')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Affective',
            fields=[
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('week', models.CharField(max_length=20, verbose_name='Week')),
                ('emoji', models.CharField(max_length=30, verbose_name='Emoji')),
                ('text', models.CharField(default='', max_length=50, verbose_name='Explanation')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
