# Generated by Django 5.0.6 on 2024-08-18 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_alter_archiveresult_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archiveresult',
            old_name='id',
            new_name='old_id',
        ),
    ]
