# Generated by Django 3.1 on 2020-08-26 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodrider', '0028_auto_20200826_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Placed'), (2, 'Confirmed'), (3, 'Ready'), (4, 'Picked Up'), (5, 'Delivered')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, default='Wt3VYFWYdemmBVc', max_length=15, null=True, unique=True),
        ),
    ]
