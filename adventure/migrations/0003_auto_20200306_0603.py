# Generated by Django 3.0.3 on 2020-03-06 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_auto_20200306_0212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='x_c',
            new_name='x_coor',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='y_c',
            new_name='y_coor',
        ),
    ]
