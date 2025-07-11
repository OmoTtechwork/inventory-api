# Generated by Django 5.2.1 on 2025-06-26 04:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiry_date', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='otp_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('category', models.CharField(max_length=50, unique=True)),
                ('price', models.FloatField()),
                ('stock_amount', models.IntegerField()),
                ('description', models.TextField()),
                ('sku_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('company_min_stock', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_product', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_status', models.CharField(default='No order yet', max_length=50)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('otp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.otp')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.productinventory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchasedItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(blank=True, choices=[('Mobile Phone', 'Phone'), ('Laptop', 'Laptop'), ('Perishable', 'Perishable'), ('Non-perishable', 'Nonperishable'), ('Native Wears', 'Native Wears'), ('Foreign Wears', 'Foreign Wears')], max_length=50, null=True)),
                ('buyer_name', models.CharField(max_length=200)),
                ('items_amount', models.IntegerField()),
                ('product_name', models.CharField(max_length=50)),
                ('top_product', models.JSONField(blank=True, null=True)),
                ('sales_status', models.CharField(default='No purchase yet', max_length=200)),
                ('items', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.productinventory')),
                ('otp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.otp')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_purchase', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockSupplied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(blank=True, choices=[('Mobile Phone', 'Phone'), ('Laptop', 'Laptop'), ('Perishable', 'Perishable'), ('Non-perishable', 'Nonperishable'), ('Native Wears', 'Native Wears'), ('Foreign Wears', 'Foreign Wears')], max_length=50, null=True)),
                ('item_name', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=50)),
                ('comments', models.TextField(blank=True)),
                ('quantity', models.IntegerField()),
                ('otp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.otp')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.productinventory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductDetailedLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount_purchased', models.IntegerField(blank=True, null=True)),
                ('amount_sold', models.IntegerField(blank=True, null=True)),
                ('stock_left', models.IntegerField(blank=True, null=True)),
                ('order_status', models.CharField(blank=True, max_length=50, null=True)),
                ('company_min_stock', models.BooleanField(blank=True, default=False, null=True)),
                ('stock_min_threshold', models.IntegerField(blank=True, null=True)),
                ('stock_in_name', models.CharField(blank=True, max_length=50, null=True)),
                ('stock_out_name', models.CharField(blank=True, max_length=50, null=True)),
                ('top_product', models.JSONField(blank=True, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ordermodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_log', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.productinventory')),
                ('stock_out', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.purchaseditems')),
                ('stock_in', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.stocksupplied')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='stocks',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.stocksupplied'),
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(max_length=100)),
                ('company_address', models.CharField(max_length=300)),
                ('item_name', models.CharField()),
                ('delivery_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.IntegerField()),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.stocksupplied')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='suppliers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.suppliers'),
        ),
    ]
