# Generated by Django 4.2.3 on 2023-07-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='slug',
            field=models.SlugField(blank=True, default=None, null=True),
        ),
    ]