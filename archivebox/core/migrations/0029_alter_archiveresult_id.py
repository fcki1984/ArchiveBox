# Generated by Django 5.0.6 on 2024-08-18 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_archiveresult_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archiveresult',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
