# Generated by Django 3.1.3 on 2021-01-14 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sc', '0016_auto_20210114_0824'),
    ]

    operations = [
        migrations.CreateModel(
            name='producthits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(blank=True, null=True, verbose_name='次数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sc.news', verbose_name='热度')),
            ],
        ),
    ]