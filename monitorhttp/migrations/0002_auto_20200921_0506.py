# Generated by Django 3.1.1 on 2020-09-20 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitorhttp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='endpoint',
            old_name='name',
            new_name='endpoint',
        ),
    ]
