# Generated by Django 3.0.3 on 2020-03-04 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_auto_20200304_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='x',
        ),
        migrations.RemoveField(
            model_name='room',
            name='y',
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]