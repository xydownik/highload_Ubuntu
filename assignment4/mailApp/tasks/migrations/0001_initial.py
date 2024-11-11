# Generated by Django 5.1.2 on 2024-11-04 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.EmailField(max_length=254, verbose_name='recipient')),
                ('subject', models.CharField(max_length=255, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('sent', models.BooleanField(default=False)),
            ],
        ),
    ]
