# Generated by Django 4.1.7 on 2023-03-09 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainpage', '0005_orderitem_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdata',
            name='review_star',
            field=models.IntegerField(default=0),
        ),
    ]
