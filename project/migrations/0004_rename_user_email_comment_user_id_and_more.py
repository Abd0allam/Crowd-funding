# Generated by Django 4.2.2 on 2023-06-10 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_projects_owner_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_email',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='donation',
            old_name='user_email',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='user_email',
            new_name='user_id',
        ),
    ]