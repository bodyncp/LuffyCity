# Generated by Django 2.0.5 on 2018-06-19 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luffy', '0005_summary_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='complete',
            field=models.BooleanField(choices=[(0, 'no'), (1, 'yes')], default=0, verbose_name='是否完成任务'),
        ),
    ]
