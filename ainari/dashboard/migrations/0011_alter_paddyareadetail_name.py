# Generated by Django 3.2.6 on 2021-09-03 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_paddyareainfo_rail_fall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paddyareadetail',
            name='name',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
