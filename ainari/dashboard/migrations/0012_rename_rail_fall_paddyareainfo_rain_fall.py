# Generated by Django 3.2.6 on 2021-09-03 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_alter_paddyareadetail_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paddyareainfo',
            old_name='rail_fall',
            new_name='rain_fall',
        ),
    ]
