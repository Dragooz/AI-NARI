# Generated by Django 3.2.6 on 2021-09-01 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_rename_resolved_paddyareariskdisease_action_taken'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paddy_images', models.ImageField(blank=True, default='default.png', upload_to='')),
            ],
        ),
    ]
