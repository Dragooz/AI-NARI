# Generated by Django 3.2.6 on 2021-09-02 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0005_auto_20210902_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('recommendation_image', models.ImageField(blank=True, default='default.png', upload_to='recommendations_images')),
            ],
        ),
        migrations.CreateModel(
            name='RiskDiseaseRecommendationRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.recommendation')),
                ('risk_disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='information.riskdisease')),
            ],
        ),
        migrations.AddField(
            model_name='recommendation',
            name='risk_disease',
            field=models.ManyToManyField(through='information.RiskDiseaseRecommendationRelationship', to='information.RiskDisease'),
        ),
    ]