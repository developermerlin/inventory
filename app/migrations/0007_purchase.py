# Generated by Django 5.1 on 2024-10-24 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_product_product_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_order', models.DateTimeField()),
                ('delivery_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Received', 'Received'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('product_supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.supplier')),
            ],
        ),
    ]