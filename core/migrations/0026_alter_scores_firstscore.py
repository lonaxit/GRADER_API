# Generated by Django 4.1.6 on 2023-07-22 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_classroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='firstscore',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
