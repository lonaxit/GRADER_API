# Generated by Django 4.1.6 on 2023-06-30 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_alter_teacherprofile_user_subjectteacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='classes', to='core.schoolclass')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.session')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.term')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='formmaster', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
