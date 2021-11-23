# Generated by Django 3.2.6 on 2021-11-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(1, 'fundacja'), (2, 'organizacja pozarządowa'), (3, 'zbiórka lokalna')], default=1)),
                ('category', models.ManyToManyField(to='charity_app.Category')),
            ],
        ),
    ]
