# Generated by Django 3.1 on 2020-08-25 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodrider', '0008_menuitemoption_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitemoption',
            name='menu',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='foodrider.menuitem'),
        ),
    ]
