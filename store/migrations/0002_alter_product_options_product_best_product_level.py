# Generated by Django 4.1 on 2022-08-24 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-level', '-price'], 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AddField(
            model_name='product',
            name='best',
            field=models.BooleanField(default=False, verbose_name='best'),
        ),
        migrations.AddField(
            model_name='product',
            name='level',
            field=models.IntegerField(default=0, verbose_name='level'),
        ),
    ]
