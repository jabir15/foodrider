# Generated by Django 3.1 on 2020-08-25 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodrider', '0010_auto_20200825_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='dish_type',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='item_type',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='option',
        ),
        migrations.AddField(
            model_name='menuitemoption',
            name='dish_type',
            field=models.CharField(choices=[('S', 'Starters'), ('M', 'Main Course'), ('D', 'Desserts')], default='M', max_length=1),
        ),
        migrations.AddField(
            model_name='menuitemoption',
            name='item_type',
            field=models.CharField(choices=[('VEG', 'Veg'), ('NVG', 'Non-Veg')], default='VEG', max_length=3),
        ),
        migrations.AddField(
            model_name='menuitemoption',
            name='menu',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='foodrider.menuitem'),
        ),
    ]
