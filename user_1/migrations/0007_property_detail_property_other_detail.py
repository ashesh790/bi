# Generated by Django 3.2.16 on 2023-01-24 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_1', '0006_delete_main_seller_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property_detail',
            fields=[
                ('property_id', models.IntegerField(primary_key=True, serialize=False)),
                ('property_type', models.CharField(max_length=150)),
                ('property_age', models.IntegerField()),
                ('selling_option', models.CharField(max_length=150)),
                ('construction_status', models.CharField(max_length=150)),
                ('floor', models.IntegerField()),
                ('bhk', models.IntegerField()),
                ('bathroom', models.IntegerField()),
                ('balcony', models.IntegerField()),
                ('furnish_type', models.CharField(max_length=150)),
                ('geography_area', models.CharField(max_length=150)),
                ('parking_type', models.CharField(max_length=150)),
                ('property_value', models.CharField(max_length=150)),
                ('property_rent_price', models.CharField(max_length=150)),
                ('from_avail_property_date', models.DateField()),
                ('property_address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Property_other_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_image_1', models.FileField(upload_to='media/')),
                ('property_image_2', models.FileField(upload_to='media/')),
                ('property_image_3', models.FileField(upload_to='media/')),
                ('media_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_1.property_detail')),
            ],
        ),
    ]