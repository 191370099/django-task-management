# Generated by Django 5.0.4 on 2024-04-21 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('developer', 'Developer'), ('qa', 'QA'), ('manager', 'Manager')], max_length=10),
        ),
    ]
