# Generated by Django 3.1 on 2020-08-26 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodrider', '0033_auto_20200826_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodrider.customer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, default='LF1i0SOM3E7aaiQ', max_length=15, null=True, unique=True),
        ),
    ]
