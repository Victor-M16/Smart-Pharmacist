# Generated by Django 5.0.3 on 2024-10-03 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_vendingmachine_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendingmachine',
            name='current_slot',
            field=models.IntegerField(null=True),
        ),
    ]
