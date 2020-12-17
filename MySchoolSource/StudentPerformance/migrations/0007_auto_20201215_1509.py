# Generated by Django 3.1.3 on 2020-12-15 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudentPerformance', '0006_auto_20201215_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chaptertopic',
            name='subject_chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentPerformance.subjectchapter'),
        ),
        migrations.AlterField(
            model_name='subjectchapter',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StudentPerformance.tblsubject'),
        ),
    ]
