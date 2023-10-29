# Generated by Django 4.2.6 on 2023-10-29 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0002_timeslot'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmerdata',
            name='procurement_center',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='farmerdata',
            name='time_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='farmers.timeslot'),
        ),
    ]