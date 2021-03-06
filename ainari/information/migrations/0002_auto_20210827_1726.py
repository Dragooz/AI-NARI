# Generated by Django 3.2.6 on 2021-08-27 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20210827_1726'),
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risk_Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RiskDiseaseSolutionRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happened', models.BooleanField()),
                ('risk_disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.risk_disease')),
            ],
        ),
        migrations.RemoveField(
            model_name='diseasesolutionrelationship',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='diseasesolutionrelationship',
            name='solution',
        ),
        migrations.RemoveField(
            model_name='risksolutionrelationship',
            name='risk',
        ),
        migrations.RemoveField(
            model_name='risksolutionrelationship',
            name='solution',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='solution',
            name='risk',
        ),
        migrations.DeleteModel(
            name='Disease',
        ),
        migrations.DeleteModel(
            name='DiseaseSolutionRelationship',
        ),
        migrations.DeleteModel(
            name='Risk',
        ),
        migrations.DeleteModel(
            name='RiskSolutionRelationship',
        ),
        migrations.AddField(
            model_name='riskdiseasesolutionrelationship',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.solution'),
        ),
        migrations.AddField(
            model_name='solution',
            name='risk_disease',
            field=models.ManyToManyField(through='information.RiskDiseaseSolutionRelationship', to='information.Risk_Disease'),
        ),
    ]
