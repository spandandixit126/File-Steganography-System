# Generated by Django 3.2.6 on 2021-10-21 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211021_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='F_usr',
            field=models.BigIntegerField(),
        ),
    ]