# Generated by Django 3.2.16 on 2023-01-28 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_1', '0010_auto_20230128_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='property_detail',
            name='seller_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user_1.user_register'),
        ),
        migrations.AlterField(
            model_name='property_detail',
            name='property_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user_register',
            name='user_id',
            field=models.CharField(max_length=11, primary_key=True, serialize=False),
        ),
    ]
