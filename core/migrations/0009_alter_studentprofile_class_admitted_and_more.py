# Generated by Django 4.1.6 on 2023-06-26 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_studentprofile_class_admitted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='class_admitted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.schoolclass'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='session_admitted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.session'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='term_admitted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.term'),
        ),
    ]
