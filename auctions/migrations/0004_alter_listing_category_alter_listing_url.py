# Generated by Django 4.1.6 on 2023-04-22 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('FSHN', 'Fashion'), ('TYS', 'Toys'), ('LCTRNCS', 'Electronics'), ('HME', 'Home'), ('BKS', 'Books'), ('STTNRY', 'Stationary'), ('THR', 'Other')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
