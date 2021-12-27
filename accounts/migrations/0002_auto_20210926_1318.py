# Generated by Django 3.2.6 on 2021-09-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=100)),
                ('emp_id', models.IntegerField()),
                ('emp_position', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='extendedusers',
            name='comp_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]