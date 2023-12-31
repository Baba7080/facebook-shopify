# Generated by Django 4.1.5 on 2023-03-29 18:19

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='confi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(default=False, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('vendor', models.CharField(max_length=50)),
                ('variants', jsonfield.fields.JSONField()),
            ],
        ),
    ]
