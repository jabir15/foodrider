# Generated by Django 3.1 on 2020-08-26 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrider', '0023_auto_20200826_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, default='TDzUnIJ15N4d7ek', max_length=15, null=True, unique=True),
        ),
    ]
