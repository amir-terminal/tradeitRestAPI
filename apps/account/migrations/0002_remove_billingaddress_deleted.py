# Generated by Django 3.1.6 on 2021-09-23 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='deleted',
        ),
    ]
