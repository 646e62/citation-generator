# Generated by Django 3.2.12 on 2023-01-16 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_rename_database_citation_citation_citation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citation',
            name='canlii_citation',
        ),
        migrations.RemoveField(
            model_name='citation',
            name='citation',
        ),
    ]
