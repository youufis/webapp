# Generated by Django 3.1.3 on 2021-02-19 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0051_auto_20210219_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userimg',
            name='image',
            field=models.ImageField(upload_to='pic/', verbose_name='图像'),
        ),
    ]
