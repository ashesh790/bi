# Generated by Django 4.1.6 on 2023-02-10 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_1", "0016_remove_p_detail_id_p_detail_property_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="p_detail",
            name="property_id",
        ),
        migrations.AddField(
            model_name="p_detail",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=0,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
    ]