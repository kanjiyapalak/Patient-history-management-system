# Generated by Django 4.2.19 on 2025-03-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_history', '0009_remove_patient_prescriptions_prescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
