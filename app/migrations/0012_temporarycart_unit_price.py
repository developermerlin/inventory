# Generated by Django 5.1 on 2024-11-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_finalcart_temporarycart'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporarycart',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
