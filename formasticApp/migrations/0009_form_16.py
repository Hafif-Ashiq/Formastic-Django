# Generated by Django 4.2.5 on 2023-10-06 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formasticApp', '0008_delete_form_16'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form_16',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('Hello_0', models.CharField()),
            ],
        ),
    ]
