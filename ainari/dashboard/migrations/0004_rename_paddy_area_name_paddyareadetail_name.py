# Generated by Django 3.2.6 on 2021-08-27 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20210827_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paddyareadetail',
            old_name='paddy_area_name',
            new_name='name',
        ),
    ]
