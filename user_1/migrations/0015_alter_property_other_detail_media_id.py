# Generated by Django 4.1.6 on 2023-02-03 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user_1", "0014_p_detail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property_other_detail",
            name="media_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="user_1.p_detail"
            ),
        ),
    ]