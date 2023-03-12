# Generated by Django 4.1.7 on 2023-03-08 11:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CartData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.date.today)),
                ('qty', models.IntegerField(default=1)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(default='', max_length=300)),
                ('product_desc', models.CharField(default='', max_length=9000)),
                ('product_img', models.ImageField(upload_to='products')),
                ('product_price', models.IntegerField(default=0)),
                ('product_cat', models.CharField(default='', max_length=100)),
                ('product_qty', models.IntegerField(default=0)),
            ],
        ),
    ]