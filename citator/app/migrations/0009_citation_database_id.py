# Generated by Django 3.2.12 on 2023-01-15 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20230115_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='citation',
            name='database_id',
            field=models.CharField(default='dd', max_length=200),
            preserve_default=False,
        ),
    ]
