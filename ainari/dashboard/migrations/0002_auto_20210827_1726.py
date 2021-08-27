# Generated by Django 3.2.6 on 2021-08-27 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaddyAreaRiskDisease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', models.FloatField()),
                ('happened', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='paddyarearisk',
            name='paddy_area_info',
        ),
        migrations.RemoveField(
            model_name='paddyarearisk',
            name='risk',
        ),
        migrations.RemoveField(
            model_name='paddyareainfo',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='paddyareainfo',
            name='risk',
        ),
        migrations.DeleteModel(
            name='PaddyAreaDisease',
        ),
        migrations.DeleteModel(
            name='PaddyAreaRisk',
        ),
        migrations.AddField(
            model_name='paddyareariskdisease',
            name='paddy_area_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.paddyareainfo'),
        ),
    ]
