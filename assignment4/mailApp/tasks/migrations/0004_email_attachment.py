# Generated by Django 5.1.2 on 2024-11-19 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_userprofile_uin_alter_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='email_attachments/'),
        ),
    ]
