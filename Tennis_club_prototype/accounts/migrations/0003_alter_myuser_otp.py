# Generated by Django 5.0.7 on 2024-10-31 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_myuser_otp_alter_myuser_otp_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='otp',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
