# Generated by Django 4.2 on 2024-03-14 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_1', '0002_delete_property_utility_v1'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_other_utils',
            name='is_brocker',
            field=models.BooleanField(default=False),
        ),
    ]
