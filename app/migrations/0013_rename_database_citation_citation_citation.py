# Generated by Django 3.2.12 on 2023-01-15 23:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_rename_style_of_cause_citation_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citation',
            old_name='database_citation',
            new_name='citation',
        ),
    ]
