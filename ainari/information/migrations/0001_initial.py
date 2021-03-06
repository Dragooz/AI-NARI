# Generated by Django 3.2.6 on 2021-08-27 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DiseaseSolutionRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RiskSolutionRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.risk')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('disease', models.ManyToManyField(through='information.DiseaseSolutionRelationship', to='information.Disease')),
                ('risk', models.ManyToManyField(through='information.RiskSolutionRelationship', to='information.Risk')),
            ],
        ),
        migrations.AddField(
            model_name='risksolutionrelationship',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.solution'),
        ),
        migrations.AddField(
            model_name='diseasesolutionrelationship',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.solution'),
        ),
    ]
