# Generated by Django 3.1.3 on 2020-12-11 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudentPerformance', '0004_auto_20201211_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperentry',
            name='subject',
            field=models.ForeignKey(default='11', on_delete=django.db.models.deletion.DO_NOTHING, to='StudentPerformance.tblsubject'),
            preserve_default=False,
        ),
    ]
