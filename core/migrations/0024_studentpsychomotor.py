# Generated by Django 4.1.6 on 2023-07-03 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0023_alter_annualresult_student_alter_classteacher_tutor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studentpsychomotor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('psychomotor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.psychomotor')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.rating')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('studentclass', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.schoolclass')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.term')),
            ],
        ),
    ]