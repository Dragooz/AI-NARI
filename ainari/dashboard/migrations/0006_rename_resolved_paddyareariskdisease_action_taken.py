# Generated by Django 3.2.6 on 2021-08-28 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_paddyareariskdisease_resolved'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paddyareariskdisease',
            old_name='resolved',
            new_name='action_taken',
        ),
    ]